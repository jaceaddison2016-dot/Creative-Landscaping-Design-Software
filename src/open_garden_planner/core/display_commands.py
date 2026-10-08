"""Undoable project presentation preferences; no geometry transforms."""

from PyQt6.QtCore import QCoreApplication

from open_garden_planner.core.commands import Command


class SetDisplayUnitsCommand(Command):
    def __init__(self, scene, units):
        self.scene, self.before, self.after = scene, scene.display_units, units

    @property
    def description(self) -> str:
        return QCoreApplication.translate("CreativePreview", "Change project units")

    def execute(self) -> None:
        self.scene.set_display_units(self.after)

    def undo(self) -> None:
        self.scene.set_display_units(self.before)


class SetPresentationCommand(Command):
    def __init__(self, scene, style: str, strength: float):
        self.scene = scene
        self.before = (scene.plant_symbol_style, scene.texture_strength)
        self.after = (style, strength)

    @property
    def description(self) -> str:
        return QCoreApplication.translate("CreativePreview", "Change drawing presentation")

    def execute(self) -> None:
        self.scene.set_presentation(*self.after)

    def undo(self) -> None:
        self.scene.set_presentation(*self.before)


class SetGridSpacingCommand(Command):
    def __init__(self, view, spacing: float):
        self.view, self.before, self.after = view, view.grid_size, spacing

    @property
    def description(self) -> str:
        return QCoreApplication.translate("CreativePreview", "Change grid spacing")

    def execute(self) -> None:
        self.view.set_grid_size(self.after)

    def undo(self) -> None:
        self.view.set_grid_size(self.before)
