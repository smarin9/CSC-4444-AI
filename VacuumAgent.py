#Vacuum-Cleaning Agent
#CSC4444 Homework 1
#Sean Marino

import random
import collections

class Thing(object):

    def __repr__(self):
        return '<{}>'.format(getattr(self, '__name__', self.__class__.__name__))

    def is_alive(self):
        "Things that are 'alive' should return true."
        return hasattr(self, 'alive') and self.alive

    def show_state(self):
        "Display the agent's internal state.  Subclasses should override."
        print("I don't know how to show_state.")


class Agent(Thing):

    def __init__(self, program=None):
        self.alive = True
        self.bump = False
        self.holding = []
        self.performance = 0
        if program is None:
            def program(percept):
                return eval(input('Percept={}; action? ' .format(percept)))
        assert isinstance(program, collections.Callable)
        self.program = program

    def can_grab(self, thing):
        """Returns True if this agent can grab this thing.
        Override for appropriate subclasses of Agent and Thing."""
        return False

def RandomAgentProgram(actions):
    "An agent that chooses an action at random, ignoring all percepts."
    return lambda percept: random.choice(actions)

def SimpleReflexAgentProgram(rules, interpret_input):
    "This agent takes action based solely on the percept. [Figure 2.10]"
    def program(percept):
        state = interpret_input(percept)
        rule = rule_match(state, rules)
        action = rule.action
        return action
    return program


def rule_match(state, rules):
    "Find the first rule that matches state."
    for rule in rules:
        if rule.matches(state):
            return rule

#Reflex Agents

#Locations A, B, and C

loc_A, loc_B, loc_C = (0, 0), (1, 0), (2, 0)

def randomAgent():
    return Agent(RandomAgentProgram(['Right', 'Left', 'Suck', 'NoOp']))

#A Simple Reflex Vacuum Agent without States 1(a)
def ReflexVacuumAgent():
    def program(percept):
        location, status = percept
        if status == 'Dirty':
            print(percept, 'Suck')
            return 'Suck'
        elif location == loc_A:
            print(percept, 'Right')
            return 'Right'
        elif location == loc_B:
            decision = random.randint(0,1)
            if decision == 0:
                print(percept, 'Left')
                return 'Left'
            elif decision == 1:
                print(percept, 'Right')
                return 'Right'
        elif location == loc_C:
            print(percept, 'Left')
            return 'Left'
    return Agent(program)

#A Simple Reflex Agent with States 1(b)
def VacuumAgentWithStates():
    cleaned = {loc_A: None, loc_B: None, loc_C: None}
    def program(percept):
        location, status = percept
        cleaned[location] = status  # Update the model here
        if cleaned[loc_A] == cleaned[loc_B] == cleaned[loc_C] == 'Clean':
            print(percept, 'NoOp')
            return 'NoOp'
        elif status == 'Dirty':
            print(percept, 'Suck')
            return 'Suck'
        elif location == loc_A and status == 'Clean':
            print(percept, 'Right')
            return 'Right'
        elif location == loc_B and status == 'Clean':
            if cleaned[loc_A] == 'Clean':
                print(percept, 'Right')
                return 'Right'
            elif cleaned[loc_C] == 'Clean':
                print(percept, 'Left')
                return 'Left'
            else:
                position = random.randint(0,1)
                if position == 0:
                    print(percept, 'Left')
                    return 'Left'
                elif position == 1:
                    print(percept, 'Right')
                    return 'Right'
        elif location == loc_C and status == 'Clean':
            print(percept,'Left')
            return 'Left'
        elif location == loc_A and (cleaned[loc_B] or cleaned[loc_C] == 'Dirty'):
            print(percept, 'Right')
            return 'Right'
        elif location == loc_B and (cleaned[loc_A] or cleaned[loc_C] == 'Dirty'):
            if cleaned[loc_A] == 'Dirty':
                print(percept, 'Left')
                return 'Left'
            elif cleaned[loc_C] == 'Dirty':
                print(percept, 'Right')
                return 'Right'
        elif location == loc_C and (cleaned[loc_A] or cleaned[loc_B] == 'Dirty'):
            print(percept, 'Left')
            return 'Left'

    return Agent(program)

#Powerful Reflex Agent 1(c)
def PowerfulAgent():
    def program(percept):
        location, status = percept
        if status[loc_A] == status[loc_B] == status[loc_C] == 'Clean' :
            print(percept, 'NoOp')
            return 'NoOp'
        elif status[location] == 'Dirty':
            print(percept, 'Suck')
            return 'Suck'
        elif location==loc_A and (status[loc_B] == 'Dirty' or status[loc_C] == 'Dirty') :
            print(percept, 'Right')
            return 'Right'
        elif location==loc_B and status[loc_A] == 'Dirty':
            print(percept, 'Left')
            return 'Left'
        elif location==loc_B and status[loc_C] == 'Dirty':
            print(percept, 'Right')
            return 'Right'
        elif location==loc_C and (status[loc_B] == 'Dirty' or status[loc_A] == 'Dirty') :
            print(percept, 'Left')
            return 'Left'

    return Agent(program)

class Dirt(Thing):
    pass

class Environment(object):

    def __init__(self):
        self.things = []
        self.agents = []

    def thing_classes(self):
        return []  # List of classes that can go into environment

    def percept(self, agent):
        '''
            Return the percept that the agent sees at this point.
            (Implement this.)
        '''
        raise NotImplementedError

    def execute_action(self, agent, action):
        "Change the world to reflect this action. (Implement this.)"
        raise NotImplementedError

    def default_location(self, thing):
        "Default location to place a new thing with unspecified location."
        return None

    def exogenous_change(self):
        "If there is spontaneous change in the world, override this."
        pass

    def is_done(self):
        "By default, we're done when we can't find a live agent."
        return not any(agent.is_alive() for agent in self.agents)

    def step(self):
        """Run the environment for one time step. If the
        actions and exogenous changes are independent, this method will
        do.  If there are interactions between them, you'll need to
        override this method."""
        if not self.is_done():
            actions = []
            for agent in self.agents:
                if agent.alive:
                    actions.append(agent.program(self.percept(agent)))
                else:
                    actions.append("")
            for (agent, action) in zip(self.agents, actions):
                self.execute_action(agent, action)
            self.exogenous_change()

    def run(self, timeHorizon=100):
        "Run the Environment for given number of time steps."
        for step in range(timeHorizon):
            if self.is_done():
                return
            self.step()

    def list_things_at(self, location, tclass=Thing):
        "Return all things exactly at a given location."
        return [thing for thing in self.things
                if thing.location == location and isinstance(thing, tclass)]

    def some_things_at(self, location, tclass=Thing):
        """Return true if at least one of the things at location
        is an instance of class tclass (or a subclass)."""
        return self.list_things_at(location, tclass) != []

    def add_thing(self, thing, location=None):
        """Add a thing to the environment, setting its location. For
        convenience, if thing is an agent program we make a new agent
        for it. (Shouldn't need to override this."""
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        assert thing not in self.things, "Don't add the same thing twice"
        thing.location = location if location is not None else self.default_location(thing)
        self.things.append(thing)
        if isinstance(thing, Agent):
            thing.performance = 0
            self.agents.append(thing)

#AgentEnvironment

class AgentEnvironment(Environment):
    """This environment has two locations, A and B. Each can be Dirty
    or Clean.  The agent perceives its location and the location's
    status. This serves as an example of how to implement a simple
    Environment."""
    def __init__(self):
        super(AgentEnvironment, self).__init__()
        self.status = {loc_A: random.choice(['Clean', 'Dirty']),
                       loc_B: random.choice(['Clean', 'Dirty']),
                       loc_C: random.choice(['Clean', 'Dirty'])}
        print('The initial configuration is:')
        print(self.status)
        print('\nSequence of Pairs: ')


    def thing_classes(self):
        return [Dirt, ReflexVacuumAgent, randomAgent,
                VacuumAgentWithStates]

    def percept(self, agent):
        "Returns the agent's location, and the location status (Dirty/Clean)."
        return (agent.location, self.status[agent.location])

#Performance Measure

    def execute_action(self, agent, action):
        if action == 'Right':
            if agent.location == loc_B:
                agent.location = loc_C
            elif agent.location == loc_A:
                agent.location = loc_B
            agent.performance -= 1
        elif action == 'Left':
            if agent.location == loc_B:
                agent.location = loc_A
            elif agent.location == loc_C:
                agent.location = loc_B
            agent.performance -= 1
        elif action == 'Suck':
            if self.status[agent.location] == 'Dirty':
                agent.performance += 10
            self.status[agent.location] = 'Clean'
        for state in self.status:
            if state == 'Dirty':
                agent.performance -= 2

    def default_location(self, thing):
        return random.choice([loc_A, loc_B, loc_C])

class PowerfulAgentEnvironment(AgentEnvironment):
    def percept(self, agent):
        return (agent.location, self.status)

def PerformanceMeasure(EnvFactory, AgentFactory, steps, runs):
    for i in range(runs):
        env = EnvFactory()
        agent = AgentFactory()
        env.add_thing(agent)
        env.run(steps)
        score = str(agent.performance)
        print("Performance Measure: ", score)
        print("")

#Problem 1(a)
print("Simple Reflex Agent without States Tests:\n")
PerformanceMeasure(AgentEnvironment, ReflexVacuumAgent, 100, 4)
print()

#Problem 1(b)
print("Simple Reflex Agent with States Tests:\n")
PerformanceMeasure(AgentEnvironment, VacuumAgentWithStates, 100, 4)
print()

#Problem 1(c)
print("Powerful Dirt Agent Tests:\n")
PerformanceMeasure(PowerfulAgentEnvironment, PowerfulAgent, 100, 4)
print()

