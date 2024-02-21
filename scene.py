from manim import *
from manim.utils.rate_functions import ease_in_expo
# from manim.mobject.geometry import *

class CoDEx(MovingCameraScene):
    def construct(self):

        # Create and add stars randomly - TODO make stars twinkle, add galaxies
        num_stars = 5000
        star_radius = 0.01
        for _ in range(num_stars):
            x = np.random.uniform(-250, 250)
            y = np.random.uniform(-5, 5)
            radius = np.random.normal(star_radius, star_radius/2)
            star = Dot(point=[x, y, 0], radius=radius, color=WHITE)
            self.add(star)

        # Timeline
        n = NumberLine(x_range=[0,200], tick_size=0)
        self.add(n)

        # initialize WD
        white_dwarf = Dot(point=[-101, 0.5, 0], radius=0.01, color=WHITE)
        self.add(white_dwarf)
        self.camera.frame.move_to([n.n2p(0)[0], 2, 0])

        # initiallize 2018 frame objects 
        p48_image = ImageMobject("media/images/darkp48.png").scale(0.35)
        p60_image = ImageMobject("media/images/darkp60.png").scale(0.45)
        galaxy1 = ImageMobject("media/images/galaxy.png").scale(0.15)
        galaxy2 = ImageMobject("media/images/galaxy.png").scale(0.15)
        galaxy3 = ImageMobject("media/images/galaxy.png").scale(0.15)
        supernova1 = Dot(radius=0.07, color=YELLOW)
        year_tick = Line(start=[n.n2p(150)[0], 0, 0], end=[n.n2p(150)[0], -1, 0])
        year_2018 = Text("2018", font_size=36).next_to(year_tick, DOWN, buff=0.1)
        
        self.add(p48_image.move_to([n.n2p(147)[0], n.get_y()+0.78, 0]),
                 p60_image.next_to(p48_image, RIGHT, buff=4),
                 galaxy1.next_to(p48_image, UP, buff=0.8).shift(RIGHT*1),
                 galaxy2.next_to(p48_image, UP, buff=1.4).shift(RIGHT*2.5),
                 galaxy3.next_to(p48_image, UP, buff=0.6).shift(RIGHT*4),
                 supernova1.next_to(galaxy2).shift(UP*0.08, LEFT*0.35),
                 year_tick, year_2018)
        
        # initialize 2023 frame objects
        year_tick = Line(start=[n.n2p(170)[0], 0, 0], end=[n.n2p(170)[0], -1, 0])
        year_2023 = Text("2023", font_size=36).next_to(year_tick, DOWN, buff=0.1)

        self.add(year_tick, year_2023)

        # opening text
        opening_text1 = Text("Nearly a billion years ago,").shift([n.n2p(0)[0], 4.7, 0])
        self.play(Write(opening_text1), run_time=2)
        self.wait(0.5)
        opening_text2 = Text("a white dwarf exploded...").shift([n.n2p(0)[0], 3.8, 0])
        self.play(Write(opening_text2), run_time=2)
        
        # exlpode white dwarf
        self.wait(1)
        self.play(white_dwarf.animate.scale(1000), run_time=2, rate_func=ease_in_expo)
        self.play(FadeOut(white_dwarf))

        # Fast forward to 2018
        self.play(self.camera.frame.animate.move_to([n.n2p(150)[0], 2, 0]), rate_func=smoothererstep, run_time=3)
        self.wait()

        # Intro to ZTF
        # self.camera.frame.move_to([n.n2p(150)[0], 2, 0])

        # Intro text
        ztf_1 = Text("In 2018, the Zwicky Transient Facility (ZTF) began scanning the sky,", font_size=32).shift([n.n2p(150)[0], 4.7, 0])
        ztf_2 = Text("searching the cosmos for the bright explosive deaths of stars: supernovae (SNe).", font_size=32).next_to(ztf_1, DOWN, buff=0.2)
        self.play(Write(ztf_1), Write(ztf_2), run_time=2)
        self.wait(4)

        # P48 text
        p48_text = VGroup(Text("The P48 telescope", font_size=26).next_to(p48_image, DOWN, buff=0.16),
                          MarkupText("<gradient from='GREEN' to='BLUE' offset='1'>discovers</gradient> new SNe", font_size=26, gradient=(GREEN, BLUE)).next_to(p48_image, DOWN, buff=0.5))
        self.play(Write(p48_text), run_time=1)
        self.wait(2)

        # Create P48 field and lines
        field = Square(side_length=1.5, color=GRAY).next_to(p48_image, UP, buff=0.3)
        field.shift(RIGHT * 1)
        p48_image_corner = p48_image.get_corner(UR) + DOWN*0.3 + LEFT*0.3
        line1 = Line(start=p48_image_corner, end=field.get_corner(UL), color=RED)
        line2 = Line(start=p48_image_corner, end=field.get_corner(DR), color=RED)
        self.play(Create(field), Create(line1), Create(line2), run_time=1)

        # Exposure flash
        exposure_flash = BackgroundRectangle(field, color=WHITE, fill_opacity=0.5)
        self.play(Uncreate(exposure_flash), run_time=0.15, rate_func=linear)
        self.wait(0.7)

        # Move to field 2 and flash
        self.play(field.animate.shift(RIGHT * 1.5),
                  line1.animate.put_start_and_end_on(start=p48_image_corner, end=line1.get_end() + RIGHT*1.5),
                  line2.animate.put_start_and_end_on(start=p48_image_corner, end=line2.get_end() + RIGHT*1.5),
                  run_time=1)
        exposure_flash = BackgroundRectangle(field, color=WHITE, fill_opacity=0.5)
        self.play(Uncreate(exposure_flash), run_time=0.15, rate_func=linear)

        # Create cutout
        # cutout = ImageMobject("media/images/SN_cutout.png").scale(1.2)
        cutout = ImageMobject("media/images/PS1_cutout.jpeg").scale(1.2)
        self.play(GrowFromPoint(cutout.next_to(galaxy1, LEFT, 2).shift(UP*0.2), 
                                supernova1.get_center()))
        # cutout_label = Text("SN Image", font_size=22, color=YELLOW).next_to(cutout, UP, 0.6)
        # self.play(Write(cutout_label))
        self.wait(0.7)

        # Move to field 3 and flash
        self.play(field.animate.shift(RIGHT * 1.5),
                  line1.animate.put_start_and_end_on(start=p48_image_corner, end=line1.get_end() + RIGHT*1.5),
                  line2.animate.put_start_and_end_on(start=p48_image_corner, end=line2.get_end() + RIGHT*1.5),
                  run_time=1)
        exposure_flash = BackgroundRectangle(field, color=WHITE, fill_opacity=0.5)
        self.play(Uncreate(exposure_flash), run_time=0.15, rate_func=linear)
        self.wait(0.7)

        # P60 text
        p60_text = VGroup(Text("And the P60 telescope", font_size=26).next_to(p60_image, DOWN, buff=0.16),
                          MarkupText("<gradient from='BLUE' to='RED' offset='1'>classifies</gradient> them", font_size=26, gradient=(BLUE, RED)).next_to(p60_image, DOWN, buff=0.5))
        self.play(Uncreate(field), Uncreate(line1), Uncreate(line2), Write(p60_text), run_time=1)
        self.wait(2)

        # Create P60 field and lines
        field = Square(side_length=0.5, color=GRAY).next_to(p60_image, UP, buff=1.3)
        field.shift(LEFT * 3.2)
        p60_image_corner = p60_image.get_corner(UL) + DOWN*0.2 + RIGHT*0.2
        line1 = Line(start=p60_image_corner, end=field.get_corner(UR), color=RED)
        line2 = Line(start=p60_image_corner, end=field.get_corner(DL), color=RED)
        self.play(Create(field), Create(line1), Create(line2), run_time=1)

        # Exposure flash
        exposure_flash = BackgroundRectangle(field, color=WHITE, fill_opacity=0.5)
        self.play(Uncreate(exposure_flash), run_time=0.15, rate_func=linear)
        self.wait(1)

        # Spectrum plot
        wav, flux, _ = np.genfromtxt("media/images/spectrum.txt", unpack=True, delimiter=' ')
        wav = ((wav - np.min(wav))/np.max(wav))
        flux = (flux - np.min(flux))/np.max(flux) + 0.1

        ax = Axes(
            x_range=[0, np.max(wav)*1.1, np.max(wav)*1.1],
            y_range=[0, np.max(flux)*2, np.max(flux)*2],
            x_length=3.5,
            y_length=1.5,
            tips=True,
            axis_config={"include_numbers": False,
                         "tip_width": 0.1,
                         "tip_height": 0.1,
                         "tip_shape": StealthTip,
                         "tick_size": 0.0}
        ).next_to(p60_image, UP, 0.4).shift(RIGHT*2)
        labels = ax.get_axis_labels(x_label='\\textrm{Wavelength}',
                                    y_label='\\textrm{Flux}').set_color(WHITE)
        
        # Wavelength label
        labels[0].next_to(ax).shift(LEFT*3.3 + DOWN*0.9)
        labels[0].scale(0.6)
        
        # Flux label
        labels[1].rotate(PI/2)
        labels[1].next_to(ax).shift(LEFT*4.1)
        labels[1].scale(0.6)
        
        # Spectrum line
        line_graph = ax.plot_line_graph(
            x_values = wav,
            y_values = flux,
            line_color=GOLD_B,
            add_vertex_dots=False,
            stroke_width = 4,
        )

        self.play(Create(ax), Create(labels), Create(line_graph), run_time=2)
        self.play(Uncreate(field), Uncreate(line1), Uncreate(line2), run_time=1)
        self.wait(2)

        # Fast forward to 2023
        self.play(self.camera.frame.animate.move_to([n.n2p(170)[0], 2, 0]), rate_func=smoothererstep, run_time=2)
        self.wait()

        # BTS sample pt1
        self.camera.frame.move_to([n.n2p(170)[0], 2, 0])

        # BTS sample pt1
        ztf_1 = Text("Years later, ZTF has discovered and classified thousands of SNe", font_size=32).shift([n.n2p(170)[0], 4.7, 0])
        ztf_2 = Text("searching the cosmos for the bright explosive deaths of stars: supernovae (SNe).", font_size=32).next_to(ztf_1, DOWN, buff=0.2)
        self.play(Write(ztf_1), Write(ztf_2), run_time=2)
        self.wait(4)

        self.wait(4)