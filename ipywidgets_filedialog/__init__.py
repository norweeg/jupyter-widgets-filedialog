import tkinter as tk
from functools import partial
from os import PathLike
from pathlib import Path
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename
from typing import Sequence, Tuple, Union

import ipywidgets
import traitlets


class FileDialog(ipywidgets.HBox, ipywidgets.widgets.widget_string._String):
    """An Interactive File Dialog Widget for Jupyter.

    Attributes:
        box_style (str, optional):
            one of 'success', 'info', 'warning' or 'danger', or ''.
            Applies a predefined style to the widget. Defaults to '',
            which applies no pre-defined style.
        description (str, optional):
            Description of the control. Defaults to "".
        initialdir (Union[str, PathLike], optional):
            The directory that the dialog starts in. Defaults to the current working directory.
        initialfile (Union[str, PathLike], optional):
            The file selected upon opening of the dialog. Defaults to "".
        filetypes (Sequence[Tuple[str,str]], optional):
            A sequence of (label, pattern) tuples, '*' wildcard is allowed.
            Defaults to [("All Files", "*.*")].
        defaultextension (str, optional):
            Default extension to append to file (save dialogs). Defaults to "".
    """

    disabled = traitlets.Bool(
        False, help="Enable or disable user changes").tag(sync=True)

    def __init__(
        self,
        box_style: str = "",
        description: str = "",
        initialdir: Union[str, PathLike] = Path.cwd(),
        initialfile: Union[str, PathLike] = "",
        filetypes: Sequence[Tuple[str, str]] = [("All Files", "*.*")],
        defaultextension: str = "",
    ):

        # Create tk interpretor and hide root window
        self._tk = tk.Tk()
        self._tk.withdraw()

        # define child widgets
        filename = ipywidgets.Text(
            description=description,
            disabled=True,
            layout=ipywidgets.Layout(width="50%"),
            style={"description_width": "initial"},
        )
        button = ipywidgets.Button(description="Browse")

        # initialize HBox superclass
        super().__init__(children=[filename, button], box_style=box_style)

        # link the value of the child widget to the value of the parent widget
        ipywidgets.link((filename, "value"), (self, "value"))
        ipywidgets.link((filename, "description"), (self, "description"))
        ipywidgets.link((button, "disabled"), (self, "disabled"))

        # link button to the dialog function
        button.on_click(
            lambda b: filename.set_trait(
                "value",
                self._dialog_function(
                    parent=self._tk,
                    title=description,
                    initialdir=initialdir,
                    initialfile=initialfile,
                    filetypes=filetypes,
                    defaultextension=defaultextension,
                ),
            )
        )

    @staticmethod
    def _dialog_function(*args, **kwargs):
        raise NotImplementedError


class OpenFileDialog(FileDialog):
    """An Interactive Open File Dialog Widget for Jupyter.

    Attributes:
        box_style (str, optional):
            one of 'success', 'info', 'warning' or 'danger', or ''.
            Applies a predefined style to the widget. Defaults to '',
            which applies no pre-defined style.
        description (str, optional):
            Description of the control. Defaults to "".
        initialdir (Union[str, PathLike], optional):
            The directory that the dialog starts in. Defaults to the current working directory.
        initialfile (Union[str, PathLike], optional):
            The file selected upon opening of the dialog. Defaults to "".
        filetypes (Sequence[Tuple[str,str]], optional):
            A sequence of (label, pattern) tuples, '*' wildcard is allowed.
            Defaults to [("All Files", "*.*")].
    """

    _dialog_function = staticmethod(askopenfilename)


class SaveFileDialog(FileDialog):
    """An Interactive Save File Dialog Widget for Jupyter.

    Attributes:
        box_style (str, optional):
            one of 'success', 'info', 'warning' or 'danger', or ''.
            Applies a predefined style to the widget. Defaults to '',
            which applies no pre-defined style.
        description (str, optional):
            Description of the control. Defaults to "".
        initialdir (Union[str, PathLike], optional):
            The directory that the dialog starts in. Defaults to the current working directory.
        initialfile (Union[str, PathLike], optional):
            The file selected upon opening of the dialog. Defaults to "".
        filetypes (Sequence[Tuple[str,str]], optional):
            A sequence of (label, pattern) tuples, '*' wildcard is allowed.
            Defaults to [("All Files", "*.*")].
        defaultextension (str, optional):
            Default extension to append to file. Defaults to "".
    """

    _dialog_function = staticmethod(asksaveasfilename)


class DirectoryDialog(FileDialog):
    """An Interactive Directory Selection Dialog Widget for Jupyter.

    Attributes:
        box_style (str, optional):
            one of 'success', 'info', 'warning' or 'danger', or ''.
            Applies a predefined style to the widget. Defaults to '',
            which applies no pre-defined style.
        description (str, optional):
            Description of the control. Defaults to "".
        initialdir (Union[str, PathLike], optional):
            The directory that the dialog starts in. Defaults to the current working directory.
        mustexist (bool, optional):
            Determines if selection must be an existing directory.  Defaults to True.
    """

    def __init__(
        self,
        box_style: str = "",
        description: str = "",
        initialdir: Union[str, PathLike] = Path.cwd(),
        mustexist: bool = True,
    ):
        self._dialog_function = partial(askdirectory, mustexist=mustexist)
        super().__init__(
            box_style=box_style,
            description=description,
            initialdir=initialdir,
        )

        filename, button = self.children

        # remove button event from superclass
        button.on_click(button._click_handlers.callbacks[0], remove=True)

        # link button to the newly-created partial dialog function
        button.on_click(
            lambda b: filename.set_trait(
                "value",
                self._dialog_function(
                    parent=self._tk,
                    title=description,
                    initialdir=initialdir,
                ),
            )
        )


__all__ = [FileDialog, SaveFileDialog, OpenFileDialog, DirectoryDialog]
