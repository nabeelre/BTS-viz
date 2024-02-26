from manim import *
from manim.utils.rate_functions import ease_in_expo, ease_in_sine

class CoDEx(MovingCameraScene):
    def construct(self):
        skip_opening = False
        skip_2018 = False
        skip_scrolling = False
        skip_mag_duration = False
        skip_ML = False

        # Timeline
        n = NumberLine(x_range=[0,300], tick_size=0)
        if skip_opening:
            self.add(n)

        # initialize scrolling objects
        year_ticks = [Line(start=[n.n2p(x)[0], 0, 0], end=[n.n2p(x)[0], -1, 0]) for x in np.arange(170,290,20)]
        year_labels = [Text(str(s), font_size=36).next_to(year_ticks[i], DOWN, buff=0.1) for i, s in enumerate(np.arange(2019,2025,1))]
        self.add(*year_ticks, *year_labels)

        if not skip_opening:
            # Create and add stars randomly - TODO make stars twinkle, add galaxies
            num_stars = 15000
            star_radius = 0.01
            for _ in range(num_stars):
                x = np.random.uniform(-50, 350)
                y = np.random.uniform(-5, 15)
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
            ztf_1 = MathTex("\\textrm{In 2018, the Zwicky Transient Facility (ZTF) and the Bright Transient Survey (BTS)}", font_size=36).shift([n.n2p(150)[0], 4.7, 0])
            ztf_2 = MathTex("\\textrm{began scanning the sky to search for supernovae (SNe), the explosive deaths of stars.}", font_size=36).next_to(ztf_1, DOWN, buff=0.1)
            self.play(Write(ztf_1), Write(ztf_2), run_time=2.5)
            self.wait(4)

            # P48 text
            p48_text = VGroup(
                MathTex("\\textrm{The P48 telescope images}", font_size=32),
                MathTex("\\textrm{large swaths of sky nightly to}", font_size=32),
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

            ML_header_text = VGroup(
                MathTex("10^6 \\textrm{ possible detections and}", font_size=26),
                MathTex("\\textrm{TBs~of~images~produced}", font_size=26),
                MathTex("\\textbf{every night}", font_size=26)
            ).arrange(DOWN*0.3).next_to(cutout, DOWN, buff=0.2)
            self.play(Uncreate(field), Uncreate(line1), Uncreate(line2), Write(ML_header_text))
            self.wait(2)

            # P60 text
            p60_text = VGroup(
                MathTex("\\textrm{Then, the P60 telescope records}", font_size=32),
                MathTex("\\textrm{their chemical signatures to}", font_size=32),  
                MarkupText("<gradient from='BLUE' to='RED' offset='1'>classify</gradient> them", 
                            font_size=26, gradient=(BLUE, RED))
            ).arrange(DOWN*0.4).next_to(p60_image, DOWN, buff=0.16)
            self.play(Write(p60_text), run_time=1)
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
            if not skip_2018:
                # Fast forward to scrolling start
                self.play(self.camera.frame.animate.move_to([n.n2p(159)[0], 2, 0]), rate_func=ease_in_sine, run_time=3)
            else:
                self.camera.frame.move_to([n.n2p(159)[0], 2, 0])

            bts_text = VGroup(
                MathTex("\\textrm{Over the years, this telescope duo and the BTS team have}", font_size=40),
                MathTex("\\textrm{discovered and classified thousands of SNe all over the sky.}", font_size=40)
            ).arrange(DOWN*0.4).move_to([n.n2p(159+5)[0], 4.8, 0])

            legend_text = VGroup(
                MathTex("\\textrm{Legend:}", font_size=34),
                VGroup(Dot(color=RED).shift(LEFT),          MathTex("\\textrm{Type Ia SNe}",        font_size=30, color=RED)),
                VGroup(Dot(color=BLUE_C).shift(LEFT*1.375), MathTex("\\textrm{Core collapse SNe}",  font_size=30, color=BLUE_C)),
                VGroup(Dot(color=GREEN).shift(LEFT*1.49),   MathTex("\\textrm{Super-luminous SNe}", font_size=30, color=GREEN)),
                VGroup(MathTex("\\textrm{Point size related to SN brightness}", font_size=30, color=WHITE))
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
            speed_modifiers = np.append(np.linspace(1,20,int(587/2)+1), 
                                        np.linspace(1,20,int(587/2)+1)[::-1])

            for frame, speed_modifier in zip(frames[1:-1], speed_modifiers):
                new_pos = cur_pos + scroll_speed*frame_time
                self.play(
                    bts_text.animate.move_to([n.n2p(new_pos)[0], 4.8, 0]),
                    legend_text.animate.move_to([n.n2p(new_pos)[0]+4.5, 2, 0]),
                    prev_frame.animate.move_to([n.n2p(new_pos)[0]-2, 2.1, 0]),
                    self.camera.frame.animate.move_to([n.n2p(new_pos)[0], 2, 0]),
                    rate_func=linear, run_time=frame_time/speed_modifier
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
                rate_func=ease_in_expo, run_time=frame_time
            )
            self.add(frame.move_to(prev_frame))
            self.remove(prev_frame)

            self.wait(4)

            # Post-scrolling text
            post_scroll_text = VGroup(
                MathTex("\\textrm{We can't search for supernovae}", font_size=30, color=WHITE),
                MathTex("\\textrm{everywhere, however.}", font_size=30, color=WHITE),
                MathTex("\\textrm{Some areas are too far south}", font_size=28, color=PURPLE_A),
                MathTex("\\textrm{Some are obscured by the Milky Way}", font_size=28, color=GREEN_B)
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
            self.play(Write(post_scroll_text[3]))
            self.play(Create(MW_plane), run_time=2)
            self.wait(0.5)

            self.play(FadeOut(frame), Uncreate(post_scroll_text), 
                      Uncreate(bts_text), Uncreate(southern_sky), 
                      Uncreate(MW_plane), run_time=2)


        if not skip_mag_duration:
            if skip_2018:
                self.camera.frame.move_to([n.n2p(270)[0], 2, 0])

            bts_sample_text = VGroup(
                Text("Still, the BTS sample now contains nearly", font_size=32, color=WHITE),
                Text("10,000 supernovae", gradient=(RED, ORANGE), font_size=46),
                Text("with publicly available classifications", font_size=28, color=WHITE)
            ).arrange(DOWN*0.4).move_to([n.n2p(270)[0], 4.8, 0])

            self.play(Write(bts_sample_text[0]))
            self.play(GrowFromCenter(bts_sample_text[1]))
            self.play(Write(bts_sample_text[2:]))
            self.wait(1.5)

            self.play(Uncreate(bts_sample_text[0]), Uncreate(bts_sample_text[2]),
                      bts_sample_text[1].animate.move_to(bts_sample_text[0]))

            file_names = [f'media/images/SNe/scatter{i}.png' for i in range(0,7)]
            scatters = [ImageMobject(scatter).move_to(bts_sample_text[1]).shift(DOWN*3 + LEFT*2) for scatter in file_names]

            legend_text = VGroup(
                Text("Legend:", font_size=28),
                VGroup(
                    Dot(color=RED).shift(LEFT), 
                    Text("Type Ia SNe", font_size=22, color=RED)
                ),
                VGroup(
                    Cross(stroke_width=8, stroke_color=BLUE_E, scale_factor=0.09).shift(LEFT*1.375), 
                    Text("Core collapse SNe", font_size=22, color=BLUE_E)
                ),
                VGroup(
                    Square(color=GREEN, fill_color=GREEN, side_length=0.1, 
                           fill_opacity=1).rotate(PI/4).shift(LEFT*1.49), 
                    Text("Super-luminous SNe", font_size=22, color=GREEN)
                ),
                VGroup(
                    RegularPolygon(n=6, color=YELLOW, fill_color=YELLOW, radius=0.075,
                                   fill_opacity=1).rotate(PI/2).shift(LEFT*0.62),  
                    Text("Novae", font_size=22, color=YELLOW)
                ),
            ).arrange(DOWN*0.5, aligned_edge=LEFT).move_to([n.n2p(274.5)[0], 2.4, 0])

            annotation_text = VGroup(
                VGroup(
                    MathTex("\\textrm{Small~range~of~intrinsic~brightness}", font_size=24, color=WHITE), 
                    MathTex("\\rightarrow", font_size=24, color=WHITE), 
                    MathTex("\\textrm{used~to~calibrate~distances}", font_size=24, color=WHITE)
                ).arrange(RIGHT*0.3),
                VGroup(
                    MathTex("\\textrm{Variety~of~stellar~properties}", font_size=24, color=WHITE), 
                    MathTex("\\rightarrow", font_size=24, color=WHITE), 
                    MathTex("\\textrm{variety~of~supernova~properties}", font_size=24, color=WHITE)
                ).arrange(RIGHT*0.3),
                VGroup(
                    MathTex("\\textrm{Rare~but}", font_size=24, color=WHITE), 
                    MathTex("\\textit{extremely}", font_size=24, color=WHITE), 
                    MathTex("\\textrm{bright}", font_size=24, color=WHITE)
                ).arrange(RIGHT*0.3),
                MathTex("\\textrm{Intrinsicly~faint,~so~only~visible~when~very~nearby}", font_size=24, color=WHITE)
            ).move_to(scatters[0])

            # Legend, axes
            self.play(FadeIn(scatters[0].scale(0.4)))
            self.wait(1)

            self.play(FadeIn(scatters[1].scale(0.4)))
            # self.play(FadeOut(scatters[0]))
            self.wait(2)

            self.play(FadeIn(scatters[2].scale(0.4)))
            # self.play(FadeOut(scatters[1]))
            self.wait(3)
            
            # Ias
            self.play(FadeIn(scatters[3].scale(0.4)), Write(legend_text[0]), 
                      Write(legend_text[1]))
            self.play(Write(annotation_text[0].shift(RIGHT*0.2)))
            # self.play(FadeOut(scatters[2]))
            self.wait(3.5)
            
            # IIs
            self.play(FadeIn(scatters[4].scale(0.4)), Write(legend_text[2]), 
                      Uncreate(annotation_text[0]))
            self.play(Write(annotation_text[1].shift(RIGHT*0.2)))
            # self.play(FadeOut(scatters[3]))
            self.wait(3.5)
            
            # SLSN
            self.play(FadeIn(scatters[5].scale(0.4)), Write(legend_text[3]), 
                      Uncreate(annotation_text[1]))
            self.play(Write(annotation_text[2].shift(RIGHT*3.5 + UP*1.5)))
            # self.play(FadeOut(scatters[4]))
            self.wait(3.5)
            
            # Novae
            self.play(FadeIn(scatters[6].scale(0.4)), Write(legend_text[4]), 
                      Uncreate(annotation_text[2]))
            self.play(Write(annotation_text[3].shift(LEFT*0.5, DOWN*0.7)))
            # self.play(FadeOut(scatters[5]))
            self.wait(4.5)

            self.play(Uncreate(annotation_text[3]))
            self.wait(4)

            self.play(Uncreate(legend_text), Uncreate(bts_sample_text[1]))
            for scatter in scatters[:-1]:
                self.remove(scatter)
            self.play(FadeOut(scatters[-1]))


        if not skip_ML:
            if skip_2018:
                self.camera.frame.move_to([n.n2p(270)[0], 2, 0])

            ML_header_text = MathTex("\\textrm{We have now fully-automated much of our real-time SN discovery and classification workflow}", font_size=32)
            ML_header_text.move_to([n.n2p(270)[0], 5.5, 0])

            self.play(Write(ML_header_text[0]), run_time=2.5)
            self.wait(4)

            # P48
            p48_image = ImageMobject("media/images/darkp48_flip.png").scale(0.35)
            p48_image.move_to([n.n2p(265)[0], n.get_y()+0.78, 0])
            p48_corner = p48_image.get_corner(UL) + DOWN*0.3 + RIGHT*0.3

            p48_obs = VGroup(
                MathTex("\\textrm{P48 robotically scans the sky}", font_size=28),
                MathTex("\\textrm{producing } 10^6 \\textrm{ possible}", font_size=28),
                MathTex("\\textrm{detections per night}", font_size=28)
            ).arrange(DOWN*0.3).next_to(p48_image, DOWN, buff=0.16)

            self.play(FadeIn(p48_image), Write(p48_obs))
            self.wait(3.5)
        
            # braai
            braai_name = MathTex("\\texttt{braai}", font_size=36)
            braai_name.next_to(p48_corner, UP, buff=3.5).shift(RIGHT*0.4)

            braai_arrow = CurvedArrow(p48_corner, 
                                      braai_name.get_left()+[-0.25,0.1,0], 
                                      angle=-PI*0.7).set_z_index(2)

            braai_cutout = ImageMobject("media/images/realbogus.png").scale(0.3)
            braai_cutout.move_to(braai_name).shift(DOWN*1.2)

            braai_descrip = VGroup(
                MathTex("\\textrm{Removes}", font_size=28),
                MathTex("\\textrm{non-astrophysical}", font_size=28),
                MathTex("\\textrm{detections}", font_size=28)
            ).arrange(DOWN*0.3).move_to(braai_name).shift(DOWN*2.5)

            self.play(Create(braai_arrow))
            self.play(Write(braai_name))

            self.play(FadeIn(braai_cutout), Write(braai_descrip))
            self.wait(4)

            # sgscore
            sgscore_name = MathTex("\\texttt{sgscore}", font_size=36)
            sgscore_name.next_to(braai_name, RIGHT, buff=2)

            sgscore_arrow = Arrow(braai_name.get_right(), sgscore_name.get_left())
            
            sgscore_tree = ImageMobject("media/images/sgscore_tree.png").scale(0.45)
            sgscore_tree.move_to(sgscore_name).shift(DOWN*1.2)

            sgscore_descrip = VGroup(
                MathTex("\\textrm{Sorts}", font_size=28),
                MathTex("\\textrm{stars and galaxies}", font_size=28),
            ).arrange(DOWN*0.3).move_to(sgscore_name).shift(DOWN*2.5)

            self.play(Create(sgscore_arrow))
            self.play(Write(sgscore_name))
            self.wait(1)

            self.play(FadeIn(sgscore_tree), Write(sgscore_descrip))
            self.wait(4)

            # BTSbot
            BTSbot_name = MathTex("\\texttt{BTSbot}", font_size=36)
            BTSbot_name.next_to(sgscore_name, RIGHT, buff=2)

            BTSbot_arrow = Arrow(sgscore_name.get_right(), BTSbot_name.get_left())
            
            BTSbot_cutouts = ImageMobject("media/images/btsbot.png").scale(0.3)
            BTSbot_cutouts.move_to(BTSbot_name).shift(DOWN*1.2)

            BTSbot_descrip = VGroup(
                MathTex("\\textrm{Selects SNe and}", font_size=28),
                MathTex("\\textrm{rejects everything else}", font_size=28),
            ).arrange(DOWN*0.3).move_to(BTSbot_name).shift(DOWN*2.5)

            self.play(Create(BTSbot_arrow))
            self.play(Write(BTSbot_name))
            self.wait(1)

            self.play(FadeIn(BTSbot_cutouts), Write(BTSbot_descrip))
            self.wait(4)

            # Draw P60 and arrow to it    
            p60_image = ImageMobject("media/images/darkp60.png").scale(0.45)
            p60_image.move_to([n.n2p(272)[0], n.get_y()+0.78, 0])
            p60_corner = p60_image.get_corner(UL) + DOWN*0.2 + RIGHT*0.2

            p60_obs = VGroup(
                MathTex("\\textrm{P60 robotically observes new}", font_size=28),
                MathTex("\\textrm{SNe suggested by } \\texttt{BTSbot}", font_size=28)
            ).arrange(DOWN*0.3).next_to(p60_image, DOWN, buff=0.16)

            p60_arrow = CurvedArrow(BTSbot_descrip.get_corner(DL)+[0.1,0,0], p60_corner,
                                    angle=PI*0.4)

            self.play(FadeIn(p60_image), Create(p60_arrow), Write(p60_obs))
            self.wait(3)

            # SNIascore
            SNIascore_name = MathTex("\\texttt{SNIascore}", font_size=36)
            SNIascore_name.next_to(BTSbot_name, RIGHT, buff=2.5)
            
            SNIascore_diagram = ImageMobject("media/images/SNIa.png").scale(0.7)
            SNIascore_diagram.move_to(SNIascore_name).shift(DOWN*1.2)

            SNIascore_descrip = VGroup(
                MathTex("\\textrm{Classifies SNe and sends}", font_size=28),
                MathTex("\\textrm{reports to the community}", font_size=28),
            ).arrange(DOWN*0.3).move_to(SNIascore_name).shift(DOWN*2.5)

            arc1 = ArcBetweenPoints(p60_image.get_corner(UR)+[-0.75, -0.3, 0], 
                                    SNIascore_descrip.get_left()+[-0.5, 1.5, 0], 
                                    angle=PI*0.25, color=WHITE)
            
            arc2 = ArcBetweenPoints(SNIascore_descrip.get_left()+[-0.5, 1.5, 0],
                                    SNIascore_name.get_left()+[-0.4, 0, 0],
                                    angle=-PI*0.5, color=WHITE)
            
            arrow_tip = ArrowTriangleFilledTip(color=WHITE)
            arrow_tip.rotate(PI).move_to(arc2.get_end())

            self.play(Create(arc1), rate_func=linear)
            self.play(Create(arc2), rate_func=linear, run_time=0.5)
            self.play(Create(arrow_tip), run_time=0.25)
            self.play(Write(SNIascore_name))
            self.wait(1)

            self.play(FadeIn(SNIascore_diagram), Write(SNIascore_descrip))
            self.wait(6)

            p60_arrow_new = CurvedArrow(BTSbot_cutouts.get_corner(DL)+[0.1,0.2,0], 
                                        p60_corner, angle=PI*0.4)

            self.play(
                Uncreate(p48_obs), Uncreate(braai_descrip), 
                Uncreate(sgscore_descrip), Uncreate(BTSbot_descrip), 
                Uncreate(p60_obs), Uncreate(SNIascore_descrip),
                ReplacementTransform(p60_arrow, p60_arrow_new)
            )

            ML_header_text2 = MathTex("\\textrm{Now, nearly a billion years after the explosion, photons from the white dwarf reach Earth}", font_size=32)
            ML_header_text2.move_to([n.n2p(270)[0], 5.5, 0])

            self.play(Uncreate(ML_header_text), Write(ML_header_text2))
            self.wait(4)

            # Create photons
            num_phots = 50
            phots_x = np.random.normal(260, 0.5, num_phots)
            phots_y = np.random.normal(15, 0.5, num_phots)
            photons = [Dot([n.n2p(p_x)[0], p_y, 0], radius=0.025, color=WHITE) for p_x, p_y in zip(phots_x, phots_y)]
            phots_t = np.random.uniform(0.5, 2.5, num_phots)
            
            # Add, move, and remove photons
            [self.add(phot) for phot in photons]
            
            move_photons = []
            for phot, t in zip(photons, phots_t):
                move_photons.append(ApplyMethod(phot.move_to, p48_corner, run_time=t))
            self.play(*move_photons, rate_func=linear)
            
            [self.remove(phot) for phot in photons]

            # highlight workflow
            self.play(braai_arrow.animate.set_fill(YELLOW_E),
                      braai_arrow.animate.set_color(YELLOW_E), run_time=0.5)
            self.play(braai_name.animate.set_fill(YELLOW_E), run_time=0.5)
            self.play(sgscore_arrow.animate.set_fill(YELLOW_E),
                      sgscore_arrow.animate.set_color(YELLOW_E), run_time=0.5)
            self.play(sgscore_name.animate.set_fill(YELLOW_E), run_time=0.5)
            self.play(BTSbot_arrow.animate.set_fill(YELLOW_E),
                      BTSbot_arrow.animate.set_color(YELLOW_E), run_time=0.5)
            self.play(BTSbot_name.animate.set_fill(YELLOW_E), run_time=0.5)
            self.play(p60_arrow.animate.set_fill(YELLOW_E),
                      p60_arrow.animate.set_color(YELLOW_E), run_time=0.5)
            self.play(arc1.animate.set_color(YELLOW_E), run_time=0.3)
            self.play(arc2.animate.set_color(YELLOW_E), 
                      arrow_tip.animate.set_fill(YELLOW_E), run_time=0.2)
            self.play(SNIascore_name.animate.set_fill(YELLOW_E), run_time=0.5)

            summary_text = VGroup(
                MathTex("\\textrm{A world first, no human}", font_size=32),
                MathTex("\\textrm{action is taken from SN}", font_size=32),
                MathTex("\\textrm{discovery to classification.}", font_size=32)
            ).arrange(DOWN*0.3).next_to(p48_image, RIGHT, buff=0.2).shift(UP*0.4)

            self.play(Write(summary_text))
            self.wait(4)

            SNIascore_arrow = Arrow(BTSbot_name.get_right(), SNIascore_name.get_left())

            self.play(
                Uncreate(ML_header_text2), Uncreate(summary_text),
                FadeOut(p48_image), FadeOut(p60_image), 
                Uncreate(arc1), Uncreate(arc2), Uncreate(arrow_tip), 
                Uncreate(p60_arrow_new), Uncreate(p60_arrow),
                Uncreate(braai_arrow), Create(SNIascore_arrow),
                braai_name.animate.set_fill(WHITE),
                sgscore_name.animate.set_fill(WHITE),
                BTSbot_name.animate.set_fill(WHITE),
                SNIascore_name.animate.set_fill(WHITE),
                sgscore_arrow.animate.set_fill(WHITE),
                sgscore_arrow.animate.set_color(WHITE),
                BTSbot_arrow.animate.set_fill(WHITE),
                BTSbot_arrow.animate.set_color(WHITE)
            )

            final_header = VGroup(
                MathTex("\\textrm{Animated by Nabeel Rehemtulla}", font_size=60),
                MathTex("\\textrm{Astronomy PhD Student advised by Adam A. Miller}", font_size=32)
            ).arrange(DOWN*0.4).move_to([n.n2p(270)[0], 9, 0])

            manim_text = VGroup(
                MathTex("\\textrm{Animated with Manim, source}", font_size=26),
                MathTex("\\textrm{code at github.com/nabeelre/BTS-viz}", font_size=26)
            ).arrange(DOWN*0.3).move_to([n.n2p(270)[0], 7.8, 0])
            
            refs_text = VGroup(
                MathTex("\\textrm{References:}", font_size=28),
                MathTex("\\textrm{Bellm et al. 2019, PASP, 131, 8002}", font_size=22),
                MathTex("\\textrm{Duev at al. 2019, MNRAS, 489, 3582}", font_size=22),
                MathTex("\\textrm{Fremling et al. 2020, ApJ, 895, 32}", font_size=22),
                MathTex("\\textrm{Fremling et al. 2021, ApJ, 917, 2}", font_size=22),
                MathTex("\\textrm{Perley et al. 2020, ApJ, 904, 35}", font_size=22),
                MathTex("\\textrm{Rehemtulla et al. 2024, arXiv:2401.15167}", font_size=22),
                MathTex("\\textrm{Tachibana \& Miller, PASP, 130, 8001}", font_size=22)
            ).arrange(DOWN*0.2, aligned_edge=LEFT).move_to([n.n2p(265.3)[0], 6.8, 0])

            credits_text = VGroup(
                MathTex("\\textrm{Other Credits:}", font_size=28),
                MathTex("\\textrm{Sky animation: Christoffer Fremling}", font_size=22),
                MathTex("\\textrm{Sky animation background: ESA/Gaia/DPAC}", font_size=22),
                MathTex("\\textrm{P48 and P60 images: ztf.caltech.edu}", font_size=22),
                MathTex("\\textrm{Color galaxy: Pan-STARRS survey}", font_size=22),
            ).arrange(DOWN*0.2, aligned_edge=LEFT).move_to([n.n2p(270)[0], 6.4, 0])

            ztf_logo = ImageMobject("media/images/ztf_logo.png")
            ciera_logo = ImageMobject("media/images/ciera.png").scale(0.44)
            isgc_logo = ImageMobject("media/images/isgc.png").scale(0.3)
            
            ztf_logo.move_to([n.n2p(273.5)[0], 6, 0])
            ciera_logo.move_to([n.n2p(274.5)[0], 7.4, 0])
            isgc_logo.move_to([n.n2p(275.5)[0], 6, 0])

            self.play(
                FadeIn(final_header[1]), FadeIn(manim_text), FadeIn(credits_text), 
                FadeIn(ztf_logo), FadeIn(ciera_logo), FadeIn(isgc_logo), FadeIn(refs_text)
            )
            
            self.play(
                self.camera.frame.animate.move_to([n.n2p(270)[0], 6.2, 0])
            )

            self.wait(1)
            self.play(Write(final_header[0]), run_time=2)

        self.wait(10)


         