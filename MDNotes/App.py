# core app
from kivymd.app import MDApp

# Widgets
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar, MDBottomAppBar
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.codeinput import CodeInput
from kivy.uix.widget import Widget
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem

from kivy.uix.rst import RstDocument
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock, ClockEvent
from kivy.metrics import dp
from kivy.lang import Builder

from pygments.lexers.markup import MarkdownLexer, RstLexer
from pygments.lexers.html import HtmlLexer

from .supported_languages import all_lexers
from markdown import markdown
import m2r

class RightContentCls(IRightBodyTouch, MDBoxLayout):
    icon = StringProperty()
    text = StringProperty()

class Item(OneLineAvatarIconListItem):
    left_icon = StringProperty()
    right_icon = StringProperty()
    right_text = StringProperty()

class MDNotes(MDApp):

    loaded: str = None
    event: ClockEvent = None

    renderingwidget: RstDocument = ObjectProperty(None)
    current_language = ObjectProperty(MarkdownLexer())
    languages_menu: MDDropdownMenu = ObjectProperty(None)

    def build(self):

        self.title = 'MDNotes - New file'
        self.theme_cls.theme_style = 'Dark'

        wdg = Builder.load_string('''<RightContentCls>
    disabled: True
    adaptive_size: True
    pos_hint: {"center_y": .5}

    MDIconButton:
        icon: root.icon
        user_font_size: "16sp"
        md_bg_color_disabled: 0, 0, 0, 0

    MDLabel:
        text: root.text
        font_style: "Caption"
        adaptive_size: True
        pos_hint: {"center_y": .5}

<Item>

    IconLeftWidget:
        icon: root.left_icon
        disabled: True

    RightContentCls:
        id: container
        icon: root.right_icon
        text: root.right_text
        
MDBoxLayout:
    orientation: "vertical"''')

        root: BoxLayout = wdg
        tbar = MDTopAppBar(title='MDNotes')
        tbar.right_action_items = [['content-save', lambda *args: None], ['arrow-collapse-left', self.to_rst], ['export-variant', lambda *args: None]]
        root.add_widget(tbar)

        frame = BoxLayout()
        self.ci = CodeInput(lexer=self.current_language, style_name='github-dark')

        self.ci.background_color= (0,0,0,0)
        frame.add_widget(self.ci)

        root.add_widget(frame)

        bbar = MDTopAppBar(type="bottom", icon='plus', mode='free-end')
        bbar.right_action_items = [['language-markdown'],['chevron-up', self.languages_menu_open]]

        root.add_widget(MDBottomAppBar(bbar, size_hint_y = None, size=[100,60]))

        self.bind(current_language=self.switch_langauge)

        self.renderingwidget = RstDocument()
        self.languages_menu = MDDropdownMenu()

        def set_lexer(self: MDNotes, lexer):
            if isinstance(lexer, str): self.current_language = all_lexers.get(lexer.lower(), None)[0]()
            else: self.current_language = lexer
            self.languages_menu.dismiss()
            self.on_language_menu_dismiss()

        menu_items = [
            {
                "text": f"Markdown",
                "left_icon":"checkbox-marked",
                "viewclass": "Item",
                "height": dp(54),
                "on_release": lambda : set_lexer(MDApp.get_running_app(), MarkdownLexer()),
            },
            {
                "text": f"HTML",
                "left_icon":"checkbox-blank",
                "viewclass": "Item",
                "height": dp(54),
                "on_release": lambda : set_lexer(MDApp.get_running_app(), HtmlLexer()),
            },
            {
                "text": f"reStructuredText",
                "viewclass": "Item",
                "left_icon":"checkbox-blank",
                "height": dp(54),
                "on_release": lambda : set_lexer(MDApp.get_running_app(), RstLexer()),
            },
            {
                "text": f"C",
                "viewclass": "Item",
                "left_icon":"checkbox-blank",
                "height": dp(54),
                "on_release": lambda : set_lexer(MDApp.get_running_app(), 'C'),
            }
            ]
        
        self.languages_menu.items = menu_items
        self.languages_menu.width_mult = 4
        self.languages_menu.radius = [10,10,10,10]

        self.languages_menu.bind(on_dismiss=self.on_language_menu_dismiss)

        return root

    def switch_langauge(self, *args):
        self.ci.lexer = self.current_language

        if all_lexers[self.current_language.name.lower()][2]: self.root.children[-1].children[-1].children[0].children[1].disabled = False
        else: self.root.children[-1].children[-1].children[0].children[1].disabled = True

        for i in self.languages_menu.items:
            if i['text'] != self.current_language.name:
                i['left_icon'] = 'checkbox-blank'
            else: 
                i['left_icon'] = 'checkbox-marked'

    def languages_menu_open(self, widget):
        self.languages_menu.caller = widget
        self.languages_menu.open()

        self.root.children[0].children[1].right_action_items.pop(-1)
        self.root.children[0].children[1].right_action_items.append(['chevron-down', self.languages_menu.dismiss])

    def on_language_menu_dismiss(self, *args):
        self.root.children[0].children[1].right_action_items.pop(-1)
        self.root.children[0].children[1].right_action_items.append(['chevron-up', self.languages_menu_open])

    def to_rst(self, instance=None):
        frame: Widget = self.ci.parent

        if not self.loaded == self.ci.text:
            self.renderingwidget.text = m2r.convert(self.ci.text)
            self.loaded == self.ci.text

            if not self.renderingwidget in frame.children:
                frame.add_widget(self.renderingwidget)
                self.event = Clock.schedule_interval(self.render_routine, 1)
                tb: MDTopAppBar = self.root.children[-1]
                tb.right_action_items.pop(1)
                tb.right_action_items.insert(1, ['arrow-collapse-right', self.close_rendering_window])

            self.renderingwidget.render()

    def close_rendering_window(self, *args):
        self.event.cancel()
        self.ci.parent.remove_widget(self.ci.parent.children[0])
        self.loaded = None
        self.root.children[-1].right_action_items.pop(1)
        self.root.children[-1].right_action_items.insert(1, ['arrow-collapse-left', self.to_rst])

    def render_routine(self, *args):
        if self.ci.text != self.loaded:
            self.to_rst()
