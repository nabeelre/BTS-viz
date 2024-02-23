from manim import *
from manim.utils.rate_functions import ease_in_expo, ease_in_sine

class CoDEx(MovingCameraScene):
    def construct(self):
        skip_opening = False
        skip_2018 = False
        skip_scrolling = False

        # Timeline
        n = NumberLine(x_range=[0,300], tick_size=0)
        if skip_opening:
            self.add(n)

        if not skip_opening:
            # Create and add stars randomly - TODO make stars twinkle, add galaxies
            num_stars = 5000
            star_radius = 0.01
            for _ in range(num_stars):
                x = np.random.uniform(-50, 350)
                y = np.random.uniform(-5, 5)
                radius = np.random.normal(star_radius, star_radius/2)
                star = Dot(point=[n.n2p(x)[0], y, 0], radius=radius, color=WHITE)
                self.add(star)

            # initialize WD
            white_dwarf = Dot(point=n.n2p(0), radius=0.01, color=WHITE).shift(UP + LEFT*2)
            self.add(white_dwarf)
            self.camera.frame.move_to([n.n2p(0)[0], 2, 0])

            # opening text
            opening_text1 = Text("Nearly a billion years ago,").shift([n.n2p(0)[0], 4.7, 0])
            self.play(Write(opening_text1), run_time=2)
            self.wait(0.5)
            opening_text2 = Text("a white dwarf exploded...").shift([n.n2p(0)[0], 3.8, 0])
            self.play(Write(opening_text2), run_time=2)
            
            # exlpode white dwarf
            self.wait(1)
            self.play(white_dwarf.animate.scale(1100), run_time=2, rate_func=ease_in_expo)
            self.add(n)
            self.play(FadeOut(white_dwarf))
            

        if not skip_2018:
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

            if not skip_opening:
                # Fast forward to 2018
                self.play(self.camera.frame.animate.move_to([n.n2p(150)[0], 2, 0]), rate_func=smoothererstep, run_time=3)
                self.wait()
            else:
                # Intro to ZTF
                self.camera.frame.move_to([n.n2p(150)[0], 2, 0])

            # Intro text
            ztf_1 = Text("In 2018, the Zwicky Transient Facility (ZTF) and the Bright Transient Survey (BTS)", font_size=28).shift([n.n2p(150)[0], 4.7, 0])
            ztf_2 = Text("began scanning the sky to search for supernovae (SNe), the explosive deaths of stars.", font_size=28).next_to(ztf_1, DOWN, buff=0.1)
            self.play(Write(ztf_1), Write(ztf_2), run_time=2.5)
            self.wait(4)

            # P48 text
            p48_text = VGroup(
                Text("The P48 telescope images", font_size=26),
                Text("large swaths of sky nightly to", font_size=26),
                MarkupText("<gradient from='GREEN' to='BLUE' offset='1'>discover</gradient> new SNe", 
                            font_size=26, gradient=(GREEN, BLUE))
            ).arrange(DOWN*0.4).next_to(p48_image, DOWN, buff=0.16)
            self.play(Write(p48_text), run_time=1.5)
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
            cutout = ImageMobject("media/images/PS1_cutout.jpeg").scale(1.2)
            self.play(GrowFromPoint(cutout.next_to(galaxy1, LEFT, 2).shift(UP*0.2), 
                                    supernova1.get_center()))
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
            p60_text = VGroup(
                Text("And the P60 telescope records", font_size=26),
                Text("their chemical signatures to", font_size=26),  
                MarkupText("<gradient from='BLUE' to='RED' offset='1'>classify</gradient> them", 
                            font_size=26, gradient=(BLUE, RED))
            ).arrange(DOWN*0.4).next_to(p60_image, DOWN, buff=0.16)
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

        if not skip_scrolling:
            # initialize scrolling objects
            year_ticks = [Line(start=[n.n2p(x)[0], 0, 0], end=[n.n2p(x)[0], -1, 0]) for x in np.arange(170,290,20)]
            year_labels = [Text(str(s), font_size=36).next_to(year_ticks[i], DOWN, buff=0.1) for i, s in enumerate(np.arange(2019,2025,1))]
            self.add(*year_ticks, *year_labels)

            if not skip_2018:
                # Fast forward to scrolling start
                self.play(self.camera.frame.animate.move_to([n.n2p(159)[0], 2, 0]), rate_func=ease_in_sine, run_time=3)
            else:
                self.camera.frame.move_to([n.n2p(159)[0], 2, 0])

            bts_text = VGroup(
                Text("Over the years, this telescope duo and the BTS team have", font_size=32),
                Text("discovered and classified thousands of SNe all over the sky.", font_size=32)
            ).arrange(DOWN*0.4).move_to([n.n2p(159+5)[0], 4.8, 0])

            legend_text = VGroup(
                Text("Legend:", font_size=28),
                VGroup(Dot(color=RED).shift(LEFT),          Text("Type Ia SNe",        font_size=22, color=RED)),
                VGroup(Dot(color=BLUE_C).shift(LEFT*1.375), Text("Core collapse SNe",  font_size=22, color=BLUE_C)),
                VGroup(Dot(color=GREEN).shift(LEFT*1.49),   Text("Super-luminous SNe", font_size=22, color=GREEN)),
                VGroup(Text("Point size related to SN brightness", font_size=22, color=WHITE))
            ).arrange(DOWN*0.5, aligned_edge=LEFT).move_to([n.n2p(159+9)[0], 2, 0])

            frames_to_render = 578  # maximum 578
            file_names = [f'media/images/frames/output{i}.jpeg' for i in np.arange(1, frames_to_render)]
            frames = [ImageMobject(frame) for frame in file_names]

            cur_pos = 159
            scroll_speed = 2.75 # frames per number line unit
            run_time = 2
            new_pos = cur_pos + scroll_speed*run_time
            self.play(
                Create(bts_text), bts_text.animate.move_to([n.n2p(new_pos)[0], 4.8, 0]),
                FadeIn(legend_text), legend_text.animate.move_to([n.n2p(new_pos)[0]+4.5, 2, 0]),
                FadeIn(frames[0].next_to(bts_text, DOWN, 0.2).shift(LEFT*3)), 
                frames[0].animate.move_to([n.n2p(new_pos)[0]-2, 2.1, 0]), 
                self.camera.frame.animate.move_to([n.n2p(new_pos)[0], 2, 0]), 
                rate_func=linear, run_time=run_time
            )
            cur_pos = new_pos

            prev_frame = frames[0]
            frame_time = 0.0667  # seconds per frame
            for frame in frames[1:-1]:
                new_pos = cur_pos + scroll_speed*frame_time
                self.play(
                    bts_text.animate.move_to([n.n2p(new_pos)[0], 4.8, 0]),
                    legend_text.animate.move_to([n.n2p(new_pos)[0]+4.5, 2, 0]),
                    prev_frame.animate.move_to([n.n2p(new_pos)[0]-2, 2.1, 0]),
                    self.camera.frame.animate.move_to([n.n2p(new_pos)[0], 2, 0]),
                    rate_func=linear, run_time=frame_time/35
                )
                cur_pos = new_pos
                self.add(frame.move_to(prev_frame))
                self.remove(prev_frame)
                prev_frame = frame

            # Last frame
            frame = frames[-1]
            self.play(
                bts_text.animate.move_to([n.n2p(270)[0], 4.8, 0]),
                legend_text.animate.move_to([n.n2p(270)[0]+4.5, 2, 0]),
                prev_frame.animate.move_to([n.n2p(270)[0]-2, 2.1, 0]),
                self.camera.frame.animate.move_to([n.n2p(270)[0], 2, 0]),
                rate_func=ease_in_expo, run_time=frame_time/4
            )
            self.add(frame.move_to(prev_frame))
            self.remove(prev_frame)

            self.wait(1)

            # Post-scrolling text
            post_scroll_text = VGroup(
                Text("We can't search for supernovae", font_size=22, color=WHITE),
                Text("everywhere, however.", font_size=22, color=WHITE),
                Text("Some areas are too far south", font_size=22, color=PURPLE_A),
                Text("Some are obscured by the Milky Way", font_size=22, color=GREEN_B)
            ).arrange(DOWN*0.4, aligned_edge=LEFT).move_to(legend_text).shift(RIGHT*0.2)

            MW_plane = Rectangle(color=GREEN_B, height=frame.height/10, width=frame.width).move_to(frames[-1])

            a = frame.get_center() + (LEFT*frame.width/40)
            b = frame.get_center() + (RIGHT*frame.width/6 + UP*frame.height/5)
            c = frame.get_center() + (DOWN*frame.height/2.2)
            d = frame.get_center() + (RIGHT*frame.width/2.8 + DOWN*frame.height/15)
            southern_sky = ArcPolygon(
                c, d, b, a, radius=3, color=PURPLE_A, 
                arc_config={"color": PURPLE_A, "radius": 3}
            )

            self.play(Uncreate(legend_text), Write(post_scroll_text[0]), 
                      Write(post_scroll_text[1]))
            self.wait(0.3)
            self.play(Write(post_scroll_text[2]))
            self.play(Create(southern_sky), run_time=2)
            self.wait(0.5)
            self.play(Write(post_scroll_text[3]), Create(MW_plane), run_time=2)
            self.wait(0.5)

            bts_sample_text = VGroup(
                Text("Still, the BTS sample now contains nearly", font_size=32, color=WHITE),
                Text("10,000 supernovae", gradient=(RED, ORANGE), font_size=46),
                Text("with publicly available spectroscopic classifications,", font_size=28, color=WHITE),
                Text("more than a single group in the world.", font_size=28, color=WHITE)
            ).arrange(DOWN*0.4).move_to(bts_text)

            self.play(FadeOut(frame), Uncreate(post_scroll_text), 
                      Uncreate(bts_text), Write(bts_sample_text[0]), 
                      Uncreate(southern_sky), Uncreate(MW_plane), run_time=2)
            self.play(GrowFromCenter(bts_sample_text[1]))
            self.play(Write(bts_sample_text[2:]))

        self.wait(4)


        # end credits to ESA/Gaia/DPAC, Christoffer Fremling, Caltech, 