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

        # initiallize p48 and p60 images
        p48_image = ImageMobject("media/images/darkp48.png").scale(0.35)
        p60_image = ImageMobject("media/images/darkp60.png").scale(0.45)
        galaxy1 = ImageMobject("media/images/galaxy.png").scale(0.15)
        galaxy2 = ImageMobject("media/images/galaxy.png").scale(0.15)
        galaxy3 = ImageMobject("media/images/galaxy.png").scale(0.15)
        supernova1 = Dot(radius=0.07, color=YELLOW)
        
        self.add(p48_image.move_to([n.n2p(147)[0], n.get_y()+0.78, 0]))
        self.add(p60_image.next_to(p48_image, RIGHT, buff=4))
        self.add(galaxy1.next_to(p48_image, UP, buff=0.8).shift(RIGHT*1))
        self.add(galaxy2.next_to(p48_image, UP, buff=1.4).shift(RIGHT*2.5))
        self.add(galaxy3.next_to(p48_image, UP, buff=0.6).shift(RIGHT*4))
        self.add(supernova1.next_to(galaxy2).shift(UP*0.08, LEFT*0.35))

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

        ztf_1 = Text("In 2018, the Zwicky Transient Facility (ZTF) began scanning the sky,", font_size=32).shift([n.n2p(150)[0], 4.7, 0])
        ztf_2 = Text("searching the cosmos for the bright explosive deaths of stars: supernovae (SNe).", font_size=32).next_to(ztf_1, DOWN, buff=0.2)
        self.play(Write(ztf_1), Write(ztf_2), run_time=2)
        self.wait(4)

        p48_text = VGroup(Text("The P48 telescope", font_size=26).next_to(p48_image, DOWN, buff=0.16),
                          MarkupText("<gradient from='RED' to='YELLOW' offset='1'>discovers</gradient> new SNe", font_size=26).next_to(p48_image, DOWN, buff=0.5))
        
        p60_text = VGroup(Text("And the P60 telescope", font_size=26).next_to(p60_image, DOWN, buff=0.16),
                          MarkupText("<b>classifies</b> them", font_size=26).next_to(p60_image, DOWN, buff=0.5))

        self.play(Write(p48_text), run_time=1)
        self.wait(2)
        self.play(Write(p60_text), run_time=1)
        self.wait(2)

        field = Square(side_length=1.5, color=GRAY).next_to(p48_image, UP, buff=0.3)
        field.shift(RIGHT * 1)
        p48_image_corner = p48_image.get_corner(UR) + DOWN*0.3 + LEFT*0.3
        line1 = Line(start=p48_image_corner, end=field.get_corner(UL), color=RED)
        line2 = Line(start=p48_image_corner, end=field.get_corner(DR), color=RED)
        self.play(Create(field), Create(line1), Create(line2), run_time=1)
        self.wait(1.5)

        self.play(field.animate.shift(RIGHT * 1.5),
                  line1.animate.put_start_and_end_on(start=p48_image_corner, end=line1.get_end() + RIGHT*1.5),
                  line2.animate.put_start_and_end_on(start=p48_image_corner, end=line2.get_end() + RIGHT*1.5),
                  run_time=1)
        self.wait(1.5)

        self.play(field.animate.shift(RIGHT * 1.5),
                  line1.animate.put_start_and_end_on(start=p48_image_corner, end=line1.get_end() + RIGHT*1.5),
                  line2.animate.put_start_and_end_on(start=p48_image_corner, end=line2.get_end() + RIGHT*1.5),
                  run_time=1)
        self.wait(1.5)


        self.wait(4)