from abc import ABC, abstractmethod


class BaseAgent(ABC):

    def __init__(self, name):

        self.name = name

    @abstractmethod
    def run(self, context):

        """
        Execute the agent's task.

        Every agent receives a context
        dictionary and returns a result.
        """

        pass
