#####################
#### BIBLIOTECAS ####
#####################

import os
import subprocess
from libqtile import hook
from libqtile import bar, layout, qtile, widget
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.config import Click, Drag, Group, Key, Match, Screen


###################
#### AUTOSTART ####
###################

@hook.subscribe.startup
def autostart():
    subprocess.Popen(["nitrogen", "--restore"])
    subprocess.Popen(["xset", "led", "named", "Scroll Lock"])
    # subprocess.Popen(["picom"])


############################
#### ATALHOS DE TECLADO ####
############################

mod = "mod4"
terminal = guess_terminal()

keys = [
    Key(
        [mod], "a",
        lazy.spawn("xset led named 'Scroll Lock'"),
        desc="Led"
    ),
    Key(
        [mod], "d",
        lazy.spawn("rofi -show drun"),
        desc="Iniciar o Rofi"
    ),
    Key(
        [mod], "p",
        lazy.spawn("flameshot"),
        desc="Iniciar o flameshot"
    ),
    Key(
        [mod], "h",
        lazy.layout.left(),
        desc="Mover o foco para a esquerda"
    ),
    Key(
        [mod], "l",
        lazy.layout.right(),
        desc="Mover o foco para a direita"
    ),
    Key(
        [mod], "j",
        lazy.layout.down(),
        desc="Mover o foco para baixo"
    ),
    Key(
        [mod], "k",
        lazy.layout.up(),
        desc="Mova o foco para cima"
    ),
    Key(
        [mod], "space",
        lazy.layout.next(),
        desc="Mover o foco da janela para outra janela"
    ),
    Key(
        [mod, "shift"], "h",
        lazy.layout.shuffle_left(),
        desc="Mover janela para a esquerda"
    ),
    Key(
        [mod, "shift"], "l",
        lazy.layout.shuffle_right(),
        desc="Mover janela para a direita"
    ),
    Key(
        [mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        desc="Mover a janela para baixo"
    ),
    Key(
        [mod, "control"], "h",
        lazy.layout.grow_left(),
        desc="Aumentar a janela para a esquerda"
    ),
    Key(
        [mod, "control"], "l",
        lazy.layout.grow_right(),
        desc="Aumentar a janela para a direita"
    ),
    Key(
        [mod, "control"], "j",
        lazy.layout.grow_down(),
        desc="Aumentar a janela para baixo"
    ),
    Key(
        [mod, "control"], "k",
        lazy.layout.grow_up(),
        desc="Grow window up"
    ),
    Key(
        [mod], "n",
        lazy.layout.normalize(),
        desc="Redefinir todos os tamanhos de janela"
    ),
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split(),
        desc="Alternar entre lados divididos e não divididos da pilha"
    ),
    Key(
        [mod], "Return",
        lazy.spawn(terminal),
        desc="Terminal de lançamento"
    ),
    Key(
        [mod], "Tab",
        lazy.next_layout(),
        desc="Alternar entre layouts"
    ),
    Key(
        [mod], "w",
        lazy.window.kill(),
        desc="Matar janela focada"
    ),
    Key(
        [mod], "f",
        lazy.window.toggle_fullscreen(),
        desc="Alternar tela cheia na janela em foco"
    ),
    Key(
        [mod], "t",
        lazy.window.toggle_floating(),
        desc="Alternar flutuação na janela em foco"
    ),
    Key(
        [mod, "control"], "r",
        lazy.reload_config(),
        desc="Recarregue a configuração"
    ),
    Key(
        [mod, "control"], "q",
        lazy.shutdown(),
        desc="Desligar Qtile"
    ),
    Key(
        [mod], "r",
        lazy.spawncmd(),
        desc="Gerar um comando usando um widget de prompt"
    ),
]

for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


################
#### GRUPOS ####
################

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        Key(
            [mod], i.name,
            lazy.group[i.name].toscreen(),
            desc=f"Switch to group {i.name}"
        ),
        Key(
            [mod, "shift"], i.name,
            lazy.window.togroup(i.name, switch_group=True),
            desc=f"Switch to & move focused window to group {i.name}"
        ),
    ])


#################
#### LAYOUTS ####
#################

layouts = [
    layout.MonadTall(
        border_focus="#ffffff",
        margin=5,
        border_width=1,
        ratio=0.50
    ),
]


#################
#### WIDGETS ####
#################

widget_defaults = dict(
    font="SymbolaRegular",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(highlight_method='text'),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(),
                widget.Clipboard(),
                widget.Clock(format="%d %B %Y, %A %H:%M"),
            ],
            24,
        ),
    ),
]


###############################
#### CONFIGURAÇÃO DO MOUSE ####
###############################

mouse = [
    Drag(
        [mod], "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position()
    ),
    Drag(
        [mod], "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size()
    ),
    Click(
        [mod], "Button2",
        lazy.window.bring_to_front()
    ),
]


##############################
#### OUTRAS CONFIGURAÇÕES ####
##############################

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24
wmname = "LG3D"
