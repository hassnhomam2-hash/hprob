from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.image import Image
from kivy.core.window import Window
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import os
import time

Window.size = (400, 700)

class ProbApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.selected_dist = None
        self.plot_image = None
        self.plot_count = 0  # To create unique filenames
        
        self.scroll = MDScrollView()
        self.main_layout = MDBoxLayout(orientation='vertical', spacing=8, padding=15, adaptive_height=True)
        
        # Title
        self.main_layout.add_widget(MDLabel(text="Probability Calculator", halign="center", font_style="H6"))
        
        # Dropdown
        self.main_layout.add_widget(MDLabel(text="Choose Distribution:", font_style="Subtitle2", size_hint_y=None, height=30))
        self.dropdown_button = MDRaisedButton(text="Select Distribution", on_release=self.open_menu, size_hint=(1, None), height=45)
        self.main_layout.add_widget(self.dropdown_button)
        
        menu_items = [
            {"text": "Normal", "viewclass": "OneLineListItem", "on_release": lambda x="Normal": self.set_distribution(x)},
            {"text": "Exponential", "viewclass": "OneLineListItem", "on_release": lambda x="Exponential": self.set_distribution(x)},
            {"text": "Uniform", "viewclass": "OneLineListItem", "on_release": lambda x="Uniform": self.set_distribution(x)},
            {"text": "Gamma", "viewclass": "OneLineListItem", "on_release": lambda x="Gamma": self.set_distribution(x)},
            {"text": "Beta", "viewclass": "OneLineListItem", "on_release": lambda x="Beta": self.set_distribution(x)},
        ]
        self.menu = MDDropdownMenu(caller=self.dropdown_button, items=menu_items, width_mult=3)
        
        # Create fresh input fields
        self.param1 = MDTextField(hint_text="", size_hint=(1, None), height=45)
        self.param2 = MDTextField(hint_text="", size_hint=(1, None), height=45)
        self.a_input = MDTextField(hint_text="a", size_hint=(1, None), height=45)
        self.b_input = MDTextField(hint_text="b", size_hint=(1, None), height=45)
        self.result_label = MDLabel(text="", halign="center", font_style="Subtitle1", size_hint_y=None, height=40)
        
        # Parameter area
        self.param_area = MDBoxLayout(orientation='vertical', spacing=5, adaptive_height=True)
        self.main_layout.add_widget(self.param_area)
        
        # Limits
        self.main_layout.add_widget(MDLabel(text="Limits:", font_style="Subtitle2", size_hint_y=None, height=30))
        self.main_layout.add_widget(self.a_input)
        self.main_layout.add_widget(self.b_input)
        
        # Calculate button
        self.calc_button = MDRaisedButton(text="Calculate", on_release=self.calculate, size_hint=(1, None), height=50)
        self.main_layout.add_widget(self.calc_button)
        
        # Result
        self.main_layout.add_widget(self.result_label)
        
        self.scroll.add_widget(self.main_layout)
        return self.scroll
    
    def open_menu(self, instance):
        self.menu.open()
    
    def set_distribution(self, dist_name):
        self.dropdown_button.text = dist_name
        self.selected_dist = dist_name
        self.menu.dismiss()
        
        # Remove old graph
        if self.plot_image:
            self.main_layout.remove_widget(self.plot_image)
            self.plot_image = None
        
        # Clear result
        self.result_label.text = ""
        
        # Clear param area and rebuild with FRESH text fields
        self.param_area.clear_widgets()
        
        self.param1 = MDTextField(hint_text="", size_hint=(1, None), height=45)
        self.param2 = MDTextField(hint_text="", size_hint=(1, None), height=45)
        
        # Clear limits
        self.a_input.text = ""
        self.b_input.text = ""
        
        if dist_name == "Normal":
            label1 = MDLabel(text="Standard deviation:", font_style="Caption", size_hint_y=None, height=20)
            label2 = MDLabel(text="mean:", font_style="Caption", size_hint_y=None, height=20)
            self.param1.hint_text = "Standard deviation"
            self.param2.hint_text = "mean"
            self.param_area.add_widget(label1)
            self.param_area.add_widget(self.param1)
            self.param_area.add_widget(label2)
            self.param_area.add_widget(self.param2)
            
        elif dist_name == "Exponential":
            label1 = MDLabel(text="parameter:", font_style="Caption", size_hint_y=None, height=20)
            self.param1.hint_text = "parameter"
            self.param_area.add_widget(label1)
            self.param_area.add_widget(self.param1)
            
        elif dist_name == "Uniform":
            label1 = MDLabel(text="lower bound:", font_style="Caption", size_hint_y=None, height=20)
            label2 = MDLabel(text="upper bound:", font_style="Caption", size_hint_y=None, height=20)
            self.param1.hint_text = "lower bound"
            self.param2.hint_text = "upper bound"
            self.param_area.add_widget(label1)
            self.param_area.add_widget(self.param1)
            self.param_area.add_widget(label2)
            self.param_area.add_widget(self.param2)
            
        elif dist_name == "Gamma":
            label1 = MDLabel(text="shape parameter:", font_style="Caption", size_hint_y=None, height=20)
            label2 = MDLabel(text="scale parameter:", font_style="Caption", size_hint_y=None, height=20)
            self.param1.hint_text = "shape parameter"
            self.param2.hint_text = "scale parameter"
            self.param_area.add_widget(label1)
            self.param_area.add_widget(self.param1)
            self.param_area.add_widget(label2)
            self.param_area.add_widget(self.param2)
            
        elif dist_name == "Beta":
            label1 = MDLabel(text="α (alpha):", font_style="Caption", size_hint_y=None, height=20)
            label2 = MDLabel(text="β (beta):", font_style="Caption", size_hint_y=None, height=20)
            self.param1.hint_text = "α (alpha)"
            self.param2.hint_text = "β (beta)"
            self.param_area.add_widget(label1)
            self.param_area.add_widget(self.param1)
            self.param_area.add_widget(label2)
            self.param_area.add_widget(self.param2)
    
    def calculate(self, instance):
        # Remove old graph
        if self.plot_image:
            self.main_layout.remove_widget(self.plot_image)
            self.plot_image = None
        
        if not self.selected_dist:
            self.result_label.text = "please choose a distribution"
            return
        
        dist_name = self.selected_dist
        
        # ----- NORMAL -----
        if dist_name == "Normal":
            try:
                s = float(self.param1.text)
            except ValueError:
                self.result_label.text = "please enter a vaild number in Standard deviation"
                return
            if s <= 0:
                self.result_label.text = "Standard deviation should be postive"
                return
            
            try:
                m = float(self.param2.text)
            except ValueError:
                self.result_label.text = "please enter a vaild number in mean"
                return
            
            dist = stats.norm(loc=m, scale=s)
        
        # ----- EXPONENTIAL -----
        elif dist_name == "Exponential":
            try:
                o = float(self.param1.text)
            except ValueError:
                self.result_label.text = "please enter a vaild number in parameter"
                return
            if o <= 0:
                self.result_label.text = "parameter should be postive"
                return
            
            dist = stats.expon(scale=o)
        
        # ----- UNIFORM -----
        elif dist_name == "Uniform":
            try:
                lower = float(self.param1.text)
            except ValueError:
                self.result_label.text = "please enter a vaild number in lower bound"
                return
            
            try:
                upper = float(self.param2.text)
            except ValueError:
                self.result_label.text = "please enter a vaild number in upper bound"
                return
            
            if lower >= upper:
                self.result_label.text = "upper bound should be greater than lower bound"
                return
            
            dist = stats.uniform(loc=lower, scale=upper-lower)
        
        # ----- GAMMA -----
        elif dist_name == "Gamma":
            try:
                al = float(self.param1.text)
            except ValueError:
                self.result_label.text = "please enter a vaild number in shape parameter"
                return
            if al <= 0:
                self.result_label.text = "shape parameter should be postive"
                return
            
            try:
                s = float(self.param2.text)
            except ValueError:
                self.result_label.text = "please enter a vaild number in shape parameter"
                return
            if s <= 0:
                self.result_label.text = "scale parameter should be postive"
                return
            
            dist = stats.gamma(a=al, scale=s)
        
        # ----- BETA -----
        elif dist_name == "Beta":
            try:
                al = float(self.param1.text)
            except ValueError:
                self.result_label.text = "please enter a vaild number in alpha"
                return
            if al <= 0:
                self.result_label.text = "alpha should be postive"
                return
            
            try:
                s = float(self.param2.text)
            except ValueError:
                self.result_label.text = "please enter a vaild number in shape parameter"
                return
            if s <= 0:
                self.result_label.text = "beta should be postive"
                return
            
            dist = stats.beta(a=al, b=s)
        
        # ----- LIMITS -----
        try:
            a = float(self.a_input.text)
        except ValueError:
            self.result_label.text = "please enter a vaild number in a"
            return
        
        try:
            b = float(self.b_input.text)
        except ValueError:
            self.result_label.text = "please enter a vaild number in b"
            return
        
        if a > b:
            self.result_label.text = "b should be greater than or equal a"
            return
        
        # ----- CALCULATE -----
        prob = dist.cdf(b) - dist.cdf(a)
        self.result_label.text = f"P(a≤x≤b)={prob:.5f}"
        
        # ----- PLOT -----
        if dist_name == "Normal":
            x_max = dist.ppf(0.9999)
            x = np.linspace(m - x_max, x_max, 900)
        elif dist_name == "Exponential":
            x_max = dist.ppf(0.999)
            x = np.linspace(0, x_max, 900)
        elif dist_name == "Uniform":
            x = np.linspace(lower - 2*abs(a), 2*abs(a) + upper, 800)
        elif dist_name == "Gamma":
            x_max = dist.ppf(0.9999)
            x = np.linspace(0, x_max, 800)
        elif dist_name == "Beta":
            x = np.linspace(0 - abs(b), 1 + abs(a), 800)
        
        y = dist.pdf(x)
        
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(x, y, 'b-', linewidth=2)
        mask = (x >= a) & (x <= b)
        ax.fill_between(x, y, where=mask, color='blue', alpha=0.4, label=f'P({a} ≤ X ≤ {b})')
        ax.legend(fontsize=8)
        ax.tick_params(labelsize=7)
        
        # Use unique filename each time to force reload
        self.plot_count += 1
        plot_path = f"plot_{self.plot_count}.png"
        plt.savefig(plot_path, dpi=120, bbox_inches='tight')
        plt.close()
        
        # Delete old plot files
        old_plot = f"plot_{self.plot_count - 1}.png"
        if os.path.exists(old_plot):
            os.remove(old_plot)
        
        # Add new graph with unique filename
        self.plot_image = Image(source=plot_path, size_hint_y=None, height=250)
        self.main_layout.add_widget(self.plot_image)

if __name__ == "__main__":
    ProbApp().run()