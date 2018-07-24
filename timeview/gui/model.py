from collections import defaultdict
from typing import List, Optional, Tuple, DefaultDict
from copy import deepcopy

from timeview.gui import rendering
from timeview.dsp import tracking


class UnknownRendererError(Exception):
    pass


class View:
    track2renderers = {
        t.__name__: {  # type: ignore  # noqa: T400
            r.name: r for r in rendering.get_renderer_classes(t)
        }
        for t in tracking.get_track_classes()
    }

    def __init__(
        self,
        track: tracking.Track,
        attached_panel: "Panel",
        renderer_name: Optional[str] = None,
        show: bool = True,
        color: Tuple[int, int, int] = (255, 255, 255),
        **parameters: str,
    ) -> None:
        self.track = track
        self.show = show
        self.panel = attached_panel
        self.renderer: Optional[rendering.Renderer] = None
        self.y_bounds = (0, 1)
        self.change_renderer(
            renderer_name
            if renderer_name is not None
            else next(iter(self.track2renderers[type(self.track).__name__])),
            **parameters,
        )
        self.color = color

    def __str__(self) -> str:
        return f"{id(self)} (with track: {id(self.track)} " f"- {self.track.path} - {self.renderer})"

    def set_color(self, color: Tuple[int, int, int]) -> None:
        self.color = color

    def change_panel(self, panel: "Panel") -> None:
        self.panel = panel

    def change_renderer(self, renderer_name: str, **parameters: str) -> None:
        # TODO: way way hackey, reconsider alternate method
        if isinstance(self.renderer, rendering.Spectrogram):
            self.renderer.prepareForDeletion()
        try:
            self.renderer = self.track2renderers[type(self.track).__name__][
                renderer_name
            ](**parameters)
        except KeyError:
            raise UnknownRendererError
        self.renderer.set_view(self, **parameters)

    def is_selected(self) -> bool:
        return self.panel.selected_view is self

    def set_selected(self) -> None:
        self.panel.set_selected_view(self)


class Panel:
    def __init__(self, model: "Model") -> None:
        self.views: List[View] = []
        self._selected_view: Optional[View] = None
        self.model = model

    def __str__(self) -> str:
        return str(id(self))

    def new_view(
        self,
        track: tracking.Track,
        renderer_name: Optional[str] = None,
        show: bool = True,
        color: Tuple[int, int, int] = (255, 255, 255),
        pos: Optional[int] = None,
        **parameters: str,
    ) -> View:
        if not pos:
            pos = len(self.views)
        self.views.insert(
            pos,
            View(
                track,
                self,
                renderer_name=renderer_name,
                show=show,
                color=color,
                **parameters,
            ),
        )
        if pos == 0:
            self.selected_view = self.views[pos]
        return self.views[pos]

    def remove_view(self, pos: int) -> View:
        view_to_remove = self.views.pop(pos)
        if not self.views:
            self.selected_view = None  # type: ignore
        elif pos == len(self.views):
            self.selected_view = self.views[-1]
        else:
            self.selected_view = self.views[pos]
        # TODO: this is way too hackey, open to suggestions to alternatives
        if isinstance(view_to_remove.renderer, rendering.Spectrogram):
            view_to_remove.renderer.prepareForDeletion()
        return view_to_remove

    def move_view(self, to_index: int, from_index: int) -> None:
        self.views.insert(to_index, self.remove_view(from_index))

    def get_selected_view(self) -> Optional[View]:
        return self._selected_view

    def set_selected_view(self, selected_view: Optional[View]) -> None:
        if self.views:
            assert selected_view in self.views
        else:
            assert selected_view is None
        self._selected_view = selected_view

    # have to tell mypy to ignore type, currently mypy only accepts read only properties
    selected_view: Optional[View] = property(  # type: ignore
        get_selected_view, set_selected_view
    )

    def selected_track(self) -> tracking.Track:
        return self.selected_view.track

    def is_selected(self) -> bool:
        return self is self.model.selected_panel

    def select_me(self) -> None:
        self.model.set_selected_panel(self)

    def get_max_duration(self) -> int:
        return max([view.track.duration / view.track.fs for view in self.views])


class Model:
    def __init__(self) -> None:
        self.panels: List[Panel] = []
        self.panel_synchronization = True
        self.selected_panel: Optional[Panel] = None

    def __str__(self) -> str:
        s = ""
        for panel in self.panels:
            for view in panel.views:
                s += f"panel: {panel}  view: {view}\n"
        return s

    def set_selected_panel(self, panel: Panel) -> None:
        assert panel in self.panels
        self.selected_panel = panel

    def new_panel(self, pos: Optional[int] = None) -> Panel:
        if not pos:
            pos = len(self.panels)
        self.panels.insert(pos, Panel(model=self))
        if len(self.panels) == 1:
            self.set_selected_panel(self.panels[pos])
        return self.panels[pos]

    def remove_panel(self, pos: int) -> Panel:
        assert bool(self.panels[pos])
        if len(self.panels) == 1:
            self.selected_panel = None
        elif pos < len(self.panels) - 2:
            self.set_selected_panel(self.panels[pos + 1])
        elif pos == len(self.panels) - 1:
            self.set_selected_panel(self.panels[pos - 1])
        return self.panels.pop(pos)

    def move_panel(self, to_index: int, from_index: int) -> None:
        self.panels.insert(to_index, self.remove_panel(from_index))

    def get_groups(self) -> DefaultDict[int, List[View]]:
        grp: DefaultDict[int, List[View]] = defaultdict(list)
        for panel in self.panels:
            for view in panel.views:
                grp[id(view.track)].append(view)
        return grp

    def get_linked_views(self, view: View) -> List[View]:
        # includes the passed argument view
        return self.get_groups()[id(view.track)]

    def move_view_across_panel(self, view: View, to_panel: Panel) -> None:

        source_panel = self.get_source_panel(view)
        pos = source_panel.views.index(view)
        view = source_panel.remove_view(pos)
        view.panel = to_panel
        to_panel.views.append(view)

    @staticmethod
    def link_track_across_panel(view: View, to_panel: Panel) -> View:
        renderer_name: Optional[str]
        if view.renderer is not None:
            renderer_name = view.renderer.name
        else:
            renderer_name = None
        new_view = to_panel.new_view(
            view.track, renderer_name, show=view.show, color=view.color
        )
        return new_view

    @staticmethod
    def copy_view_across_panel(view: View, to_panel: Panel) -> None:
        color = view.color
        track = deepcopy(view.track)
        renderer = view.renderer
        show = view.show
        renderer_name: Optional[str]
        if renderer is not None:
            renderer_name = renderer.name
        else:
            renderer_name = None
        to_panel.new_view(track, renderer_name, show=show, color=color)

    def get_source_panel(self, view: View) -> Panel:
        for panel in self.panels:
            if view in panel.views:
                return panel
        else:
            raise IndexError

    def move_view_within_panel(self, view: View, position: int) -> None:
        panel = self.get_source_panel(view)
        panel.views.remove(view)
        panel.views.insert(position, view)
