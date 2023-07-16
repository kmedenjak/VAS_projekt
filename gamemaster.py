import time
import random
import asyncio
import spade
from spade import wait_until_finished
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import FSMBehaviour, State

class Gamemaster(Agent):

    class FSMAgentBehaviour(FSMBehaviour): 
        async def on_start(self):
        # postavi sve agente
            self.player1 = "kmedenjak_agent1@5222.de"
            self.player2 = "kmedenjak_agent2@5222.de"
            self.player3 = "kmedenjak_agent3@5222.de"
            self.player4 = "kmedenjak_agent4@5222.de"
            self.player5 = "kmedenjak_agent5@5222.de"
            self.player6 = "kmedenjak_agent6@5222.de"
            self.agent.agenti = [self.player1, self.player2, self.player3, self.player4, self.player5, self.player6]
            self.agent.igraci = []
            self.agent.parovi = []
            self.agent.odgovori = {}
            self.agent.preostali = []
            self.agent.brojIspadanje = 0
            self.agent.brojParova = 0

        async def on_end(self):
            print("Shutting down Gamemaster")

    class StateOne(State):
        async def run(self):
            print("I'm at state one (initial state)")
            
            def getPlayers():
                number = 0
                while (int(number) < 3 or int(number) > 6):
                    number = int(input('Choose number of players between 3 and 6 \n'))
                return random.sample(self.agent.agenti, number)
            randomPlayers = getPlayers()
            for p in randomPlayers:
                print(p)

            self.agent.igraci = randomPlayers

            if len(randomPlayers) == 3:
                self.agent.brojParova = 1
            elif len(randomPlayers) == 4 or len(randomPlayers) == 5:
                self.agent.brojParova = 2
            else:
                self.agent.brojParova = 3

            igraci = ""
            zadnji = self.agent.igraci[-1]
            for p in self.agent.igraci:
                if(p == zadnji):
                    igraci += f"{p}"
                else:
                    igraci += f"{p},"

            for p in self.agent.igraci:
                msg = Message(to=p, body = "igraju")
                msg.set_metadata("salje", "gamemaster")
                msg.set_metadata("igraci", igraci)
                await self.send(msg)              

            gameType = 0
            while (gameType != 1 and gameType !=2):
                gameType = int(input('Press: \n 1. Forming pairs \n 2. Dropping players \n'))
            
            if(gameType == 1):
                print('Forming pairs')
                self.set_next_state("state2")
            elif(gameType == 2):
                print('Dropping players')
                self.agent.brojIspadanje = 0
                while (self.agent.brojIspadanje < 2 or self.agent.brojIspadanje > len(self.agent.igraci)):
                    self.agent.brojIspadanje = int(input('How many players needed for the game? \n'))
                self.set_next_state("state4")

    class StateTwo(State):
        async def run(self):
            while(len(self.agent.parovi) != self.agent.brojParova):
                self.agent.odgovori = {}
                print("I'm at state two")
                for p in self.agent.igraci:
                    msg = Message(to=p, body = "igra")
                    msg.set_metadata("salje", "gamemaster")
                    await self.send(msg)
                    await asyncio.sleep(2)
                    odg = await self.receive(timeout=10)
                    self.agent.odgovori[odg.get_metadata("salje")] = odg.body
                                      
                print("Poruke poslane")

                #Grupiranje agenata po vrijednosti
                odgovori = {}
                for a, o in self.agent.odgovori.items():
                    if o in odgovori:
                        odgovori[o].append(a)
                    else:
                        odgovori[o] = [a]

                #Uparivanje agenata
                for o, a in odgovori.items():
                    if len(a) == 2:
                        self.agent.parovi.append(a)
                        p1, p2 = a
                        self.agent.igraci.remove(p1)
                        self.agent.igraci.remove(p2)
                        self.agent.odgovori = {}
            
            self.set_next_state("state3")

    class StateThree(State):
        async def run(self):
            print("Parovi:")
            i = 1
            for p in self.agent.parovi:
                p1, p2 = p
                print(f"Par {i}: {p1} i {p2}")
                i += 1
                msg = Message(to=p1, body = f"U paru si s {p2}")
                msg.set_metadata("salje", "gamemaster")
                await self.send(msg)
                msg = Message(to=p2, body = f"U paru si s {p1}")
                msg.set_metadata("salje", "gamemaster")
                await self.send(msg)

            self.set_next_state("state6")

    class StateFour(State):
        async def run(self):
            rezultat = False
            while rezultat is False:
                self.agent.odgovori = {}
                rezultat = False
                for p in self.agent.igraci:
                    msg = Message(to=p, body = "igra")
                    msg.set_metadata("salje", "gamemaster")
                    await self.send(msg)
                    await asyncio.sleep(2)
                    odg = await self.receive(timeout=10)
                    self.agent.odgovori[odg.get_metadata("salje")] = odg.body
                    
                print("Poruke poslane")

                odgovori = {}
                for a, o in self.agent.odgovori.items():
                    if o in odgovori:
                        odgovori[o].append(a)
                    else:
                        odgovori[o] = [a]

                for o, a in odgovori.items():
                    if len(a) == self.agent.brojIspadanje:
                        self.agent.preostali = a
                        self.agent.odgovori = {}
                        rezultat = True

            self.set_next_state("state5")


    class StateFive(State):
        async def run(self):
            print(self.agent.preostali)
            for p in self.agent.preostali:
                msg = Message(to=p, body = f"Preostali igrači su: {self.agent.preostali}")
                msg.set_metadata("salje", "gamemaster")
                await self.send(msg)

            self.set_next_state("state6")

    class StateSix(State):
        async def run(self):
            for p in self.agent.agenti:
                print(f"Saljem agentu {p} poruku za kraj")
                msg = Message(to=p, body = "kraj")
                msg.set_metadata("salje", "gamemaster")
                await self.send(msg)

            await self.agent.stop()

    async def setup(self):
        print("Agent starting . . .")
        fsm = self.FSMAgentBehaviour()
        fsm.add_state(name="state1", state=self.StateOne(), initial=True)
        fsm.add_state(name="state2", state=self.StateTwo())
        fsm.add_state(name="state3", state=self.StateThree())
        fsm.add_state(name="state4", state=self.StateFour())
        fsm.add_state(name="state5", state=self.StateFive())
        fsm.add_state(name="state6", state=self.StateSix())
        fsm.add_transition(source="state1", dest="state2")
        fsm.add_transition(source="state1", dest="state4")
        fsm.add_transition(source="state2", dest="state2")
        fsm.add_transition(source="state2", dest="state3")
        fsm.add_transition(source="state3", dest="state6")
        fsm.add_transition(source="state4", dest="state4")
        fsm.add_transition(source="state4", dest="state5")
        fsm.add_transition(source="state5", dest="state6")
        self.add_behaviour(fsm)

    

async def main():
    
    gamemaster = Gamemaster("kmedenjak_igra@5222.de", "12345")

    await gamemaster.start()

    await spade.wait_until_finished(gamemaster)
    await gamemaster.stop()

if __name__ == "__main__":
    spade.run(main())