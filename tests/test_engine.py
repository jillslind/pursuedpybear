import unittest
from unittest import mock

from pygame import Surface

from ppb import GameEngine, BaseScene
from ppb.events import Quit
from ppb.systems import System

CONTINUE = True
STOP = False


@unittest.skip
class TestEngine(unittest.TestCase):

    def test_initialize(self):
        pass

    def test_start(self):
        mock_scene = mock.Mock(spec=BaseScene)
        mock_scene.background_color = (0, 0, 0)
        mock_scene_class = mock.Mock(spec=BaseScene, return_value=mock_scene)
        engine = GameEngine(mock_scene_class)
        engine.display = mock.Mock(spec=Surface)
        engine.start()
        self.assertIs(engine.current_scene, mock_scene)


@unittest.skip
class TestEngineSceneActivate(unittest.TestCase):

    def setUp(self):
        self.mock_scene = mock.Mock(spec=BaseScene)
        self.mock_scene.background_color = (0, 0, 0)
        self.mock_scene_class = mock.Mock(return_value=self.mock_scene)
        self.engine = GameEngine(self.mock_scene_class)
        self.engine.display = mock.Mock(spec=Surface)
        self.engine.start()

    def test_continue_running(self):
        """
        Test that a Scene.change that returns (True, {}) doesn't change
        state.
        """
        self.mock_scene.change = mock.Mock(return_value=(CONTINUE, {}))
        self.engine.manage_scene()
        self.assertIs(self.engine.current_scene, self.mock_scene)

    def test_stop_scene_no_new_scene(self):
        """
        Test a Scene.change that returns (False, {}) leaves the scene
        stack empty.
        """
        self.mock_scene.change = mock.Mock(return_value=(STOP, {}))
        self.engine.manage_scene()
        self.assertIsNone(self.engine.current_scene)

    def test_next_scene_none(self):
        self.mock_scene.change = mock.Mock(return_value=(CONTINUE,
                                                         {"scene_class": None}
                                                         )
                                           )
        self.engine.manage_scene()
        self.assertIs(self.engine.current_scene, self.mock_scene)


def test_signal():

    class Quitter(System):

        def activate(self, engine):
            yield Quit()

    engine = GameEngine(BaseScene, systems=[Quitter()])
    engine.run()
    assert not engine.running
