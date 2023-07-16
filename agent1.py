import time
import random
import asyncio
import spade
from pyprobs import Probability
from spade import wait_until_finished
from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

class Agents(Agent):
    class MyBehav(CyclicBehaviour):
        async def on_start(self):
            print("Pokretanje cyclic")
            self.agent.igraju = []
            self.agent.svida = ""
            self.agent.svidaOdgovori = []
            self.agent.firstMessage = True

        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"Message received with content: {msg.body} from {msg.get_metadata('salje')}")
                if(msg.body == "igra" and msg.get_metadata('salje') == "gamemaster"):
                    odgovor = msg.make_reply()
                    odgovor.set_metadata("salje", "kmedenjak_agent1@5222.de")
                    if self.agent.firstMessage:
                        odgovor.body = f"{Probability.prob(80/100)}"
                        self.agent.firstMessage = False
                    else:
                        brojTrue = 0
                        for o in self.agent.svidaOdgovori:
                            if o == "True":
                                brojTrue += 1
                        vjerojatnost = round(((round(brojTrue / len(self.agent.svidaOdgovori)) * 100) + 80) / 2)
                        odgovor.body = f"{Probability.prob(vjerojatnost/100)}"
                    print(odgovor.body)
                    await self.send(odgovor)
                    for i in self.agent.igraju:
                        odgovor.to = i
                        await self.send(odgovor)
                elif(msg.get_metadata('salje') == self.agent.svida):
                    self.agent.svidaOdgovori.append(msg.body)
                elif(msg.body == "igraju"):
                    igraciSplit = msg.get_metadata("igraci").split(",")
                    for i in igraciSplit:
                        if i != "kmedenjak_agent1@5222.de":
                            self.agent.igraju.append(i)
                    self.agent.svida = random.choice(self.agent.igraju)
                    print(f"Svida: {self.agent.svida}")
                elif(msg.body == "kraj"):
                    await self.agent.stop()
            await asyncio.sleep(1)

    async def setup(self):
        print("Agent 1 pokrenut")
        self.behav = self.MyBehav()
        self.add_behaviour(self.behav)

async def main():
    
    agent = Agents("kmedenjak_agent1@5222.de", "12345")

    await agent.start()
    print("Receiver started")

    await spade.wait_until_finished(agent)
    print("Agents finished")

if __name__ == "__main__":
    spade.run(main())


