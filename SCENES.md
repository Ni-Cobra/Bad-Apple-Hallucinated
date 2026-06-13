# Bad Apple!! — Complete Scene-by-Scene Breakdown (Single Source of Truth)

## Video metadata

| Property | Value |
|---|---|
| Title | 【東方】Bad Apple!! ＰＶ【影絵】 ("[Touhou] Bad Apple!! PV [Shadow Art]") |
| Original creator | あにら (Anira) — 3D modeling & animation; storyboard/scene concept by Μμ |
| Original upload | Nico Nico Douga sm8628149, October 27, 2009 |
| Total duration | **3:39 (219 s)** — verified against YouTube reprint FtutLA63Cp8 (`lengthSeconds: 219`) |
| Frame range @30fps | **0–6569** (frame = floor(seconds × 30)); reference frame dump used for verification has 6572 frames at exactly 30 fps |
| Style | Monochrome shadow art: every element is a solid black or solid white silhouette on the opposite-color background. Soft gaussian-blurred edges; occasional gray used only for glows, smoke/fire texture, and floor shadows |
| Music (timing reference ONLY — our recreation is silent) | "Bad Apple!! feat. nomico" (Alstroemeria Records, vocals nomico), PV-size edit, ≈138 BPM |
| Cast | 36 character appearances, presented in chronological order of the Touhou games they debuted in (Windows era TH06→TH10.5, then PC-98 era), ending with a loop back to Reimu |
| Reference frames | 97 verified still frames downloaded to `_ref_frames/` (named `t<seconds>_f<frame#>.jpg`, 1-indexed frame numbers from the bleov/bad-apple-frames repo; subtract 1 for 0-indexed) |

**Core design language (applies everywhere):** one silhouette MORPHS into the next (object-to-character morphs: apple core→Patchouli, finger→Remilia, teacup shard→Sakuya, knife→Flandre's wing, petal→boat, rod→Mokou, pen→Suika's horn, sake drop→Alice, doll→Nitori, splash→petals, parasol→scythe, water column→PC-98 Reimu, the pair→yin-yang orb). Black/white polarity inverts frequently, usually exactly on a morph or a musical accent.

## Musical section map (timing anchors for the silent recreation)

Derived from the 138 BPM grid (1 bar ≈ 1.739 s, first downbeat ≈ t+0.7 s) and locked to five independently sourced character-timestamp lists. Every boundary below coincides with a verified on-screen event.

| Section | Time | Seconds | Frames @30fps | On-screen event at boundary |
|---|---|---|---|---|
| Instrumental intro | 0:00.0–0:28.6 | 0.0–28.6 | 0–858 | black screen → Reimu → Marisa flight |
| Verse 1 (A1+A2, 16 bars) | 0:28.6–0:56.4 | 28.6–56.4 | 858–1692 | starts as apple core morphs into Patchouli |
| Verse 2 (B1+B2, 16 bars) | 0:56.4–1:24.2 | 56.4–84.2 | 1692–2526 | starts on Youmu ("夢見てる" / Youmu pun); ends on lyric "黒にする" (turn black) |
| Chorus 1 (16 bars) | 1:24.2–1:52.1 | 84.2–112.1 | 2526–3363 | starts as Rod of Remorse morphs into Mokou; ends on "白になる" (turn white) → screen washes to pure white |
| Instrumental interlude (8 bars) | 1:52.1–2:06.0 | 112.1–126.0 | 3363–3780 | Prismriver "band" performance begins exactly here (documented sync point) |
| Verse 3/4 (16 bars) | 2:06.0–2:33.8 | 126.0–153.8 | 3780–4614 | starts as leaves fall / Sanae sweeps |
| Chorus 2 (16 bars) | 2:33.8–3:01.7 | 153.8–181.7 | 4614–5451 | starts as the Yukari/Tenshi negative space becomes Aya's wing |
| Final chorus, key change up (16 bars) | 3:01.7–3:29.5 | 181.7–209.5 | 5451–6285 | key change lands exactly on splash→petals→Yuka reveal (documented sync point) |
| Instrumental outro | 3:29.5–3:39.0 | 209.5–219.0 | 6285–6569 | yin-yang orb → final Marisa/Reimu → zoom to black (loops to frame 0) |

---

## Scene list (complete, gapless, 0:00–3:39)

Conventions: timestamps mm:ss; `[s]` = seconds; `[f]` = frames @30fps (floor(s×30)). "W-on-B" = white silhouettes on black background; "B-on-W" = black silhouettes on white background. Confidence is HIGH unless flagged. ★ = iconic moment.

### Scene 1 — Black screen / zoom-out reveal ★ (loop point)
- **0:00–0:04** | [0.0–4.0 s] | [f 0–120]
- **Characters:** Reimu Hakurei (revealed)
- **Action:** The video opens on a SOLID BLACK screen (verified f15). The camera pulls back and the blackness is revealed to be Reimu's silhouette from behind (big hair bow, detached sleeves) — by f120 she is a full-figure black silhouette. Because the ending zooms INTO Reimu's black silhouette, the video forms a perfect loop; at the loop point the apple from the final shot is in her hand here.
- **Polarity:** solid black → resolves to **B-on-W**.
- **Transition in/out:** loop from end / continuous into Scene 2.

### Scene 2 — Reimu's intro dance with the apple ★
- **0:04–0:15** | [4.0–15.0 s] | [f 120–450]
- **Characters:** Reimu Hakurei
- **Action:** Reimu sways/dances to the beat holding an apple. ~0:08 (verified f241): close-up profile, she raises the apple to her mouth as if to bite it. She decides not to, winds up (motion-blur spin verified f361 at 0:12) and **tosses the apple high into the sky** (~0:13–0:15; apple alone airborne verified f436).
- **Props:** the apple (central motif).
- **Polarity:** **B-on-W**.
- **Transition out:** the airborne apple is caught mid-flight by Marisa; the cut/morph at ~0:15–0:16 carries a full polarity inversion (mixed-polarity transitional frame verified f481).

### Scene 3 — Marisa's broom flight to the Scarlet Devil Mansion ★
- **0:15–0:28.5** | [15.0–28.5 s] | [f 450–855]
- **Characters:** Marisa Kirisame
- **Action:** Marisa swoops in on her broom and catches Reimu's apple. She flies right-to-left across a **starry night sky** (white star specks on black, verified f601 — witch hat, braid, broom bristles all readable in silhouette). The silhouette of the **Scarlet Devil Mansion** (towers, gate) rises from the lower-left as she descends toward it (verified f721 at 0:24). She eats the apple during the flight and casually **drops the core**, which falls alone through the black frame (verified f811 at 0:27) and bounces once.
- **Props:** broom, witch hat, apple → apple core; SDM building; star field.
- **Polarity:** **W-on-B** (with white star dots — the only "particle field" backdrop in the video).
- **Transition out:** the falling core bounces and morphs into Patchouli exactly at the verse-1 downbeat.

### Scene 4 — Patchouli's dance (VERSE 1 begins)
- **0:28.5–0:36** | [28.5–36.0 s] | [f 855–1080]
- **Characters:** Patchouli Knowledge
- **Action:** The apple core transforms into Patchouli (vocals begin). She dances in place with flowing hand gestures (full body verified f871; mob cap + extended arm verified f961). The passage ends on a close-up of her profile with one **index finger raised, wagging** (verified f1051 at 0:35).
- **Polarity:** **B-on-W** (flips back from Scene 3 at the morph).
- **Transition out:** her raised finger morphs directly into Remilia.

### Scene 5 — Remilia and the teacup
- **0:36–0:42.5** | [36.0–42.5 s] | [f 1080–1275]
- **Characters:** Remilia Scarlet
- **Action:** Remilia appears (mob cap with ribbon, short hair) and spreads her **scalloped bat wings** (verified f1111 at 0:37). Close-up profile: she holds a teacup out on her hand (verified f1201 at 0:40) and **lets it drop**.
- **Props:** bat wings, teacup.
- **Polarity:** **B-on-W**.
- **Transition out:** the teacup falls and **shatters**; the shatter is the polarity inversion.

### Scene 6 — Sakuya: shards, twirl, knives
- **0:42.5–0:50** | [42.5–50.0 s] | [f 1275–1500]
- **Characters:** Sakuya Izayoi
- **Action:** White teacup shards scatter across the black frame (verified f1291 at 0:43). One shard morphs into a small spinning figure with outstretched arms seen from an odd top-down angle (verified f1336 at 0:44.5) — famously mistaken for Rumia, but frame analysis and the original storyboard confirm it is **Sakuya twirling** (the "ribbon" is her apron and the arms show maid-frill cuffs; storyboard reads "Sakuya casting The World"). She lands facing the camera as the maid (headband visible, verified f1381 at 0:46), draws her **throwing knives** and hurls them (~0:48–0:50, rear view verified f1441).
- **Props:** teacup shards, throwing knives, maid headband/apron.
- **Polarity:** **W-on-B** (inverted at the teacup shatter, ~0:42–0:43).
- **Transition out:** the tip of one thrown knife morphs into the tip of Flandre's wing.

### Scene 7 — Flandre: wings, inversion, the "slice" ★
- **0:50–0:57** | [50.0–57.0 s] | [f 1500–1710]
- **Characters:** Flandre Scarlet
- **Action:** Close-up: a row of Flandre's **crystal-drop wing prongs** emerges from the knife tip (verified f1516 at 0:50.5). Pull back: Flandre (side ponytail) spreads her arms and shows both open hands (verified f1591 at 0:53). On the accent ~0:54 the **whole frame inverts** and she breaks into her mad grin; at ~0:55.5 a horizontal **blade flash crosses her chest** (verified f1666) — it reads as her being "sliced", though it is actually a sword appearing across her chest (this blade is Youmu's).
- **Props:** crystal wings, blade flash.
- **Polarity:** **W-on-B** (0:50–0:54) → **inverts mid-scene to B-on-W** (0:54–0:57). One of only two mid-scene inversions on a held character.
- **Transition out:** the slicing blade belongs to Youmu, who carries the cut into Scene 8 (with another flip back to W-on-B).

### Scene 8 — Youmu's sword flourish (VERSE 2 begins — "夢見てる" / Youmu pun)
- **0:57–1:04** | [57.0–64.0 s] | [f 1710–1920]
- **Characters:** Youmu Konpaku (foreground), Yuyuko Saigyouji (background from ~0:59)
- **Action:** Youmu stands center holding her two swords (Roukanken & Hakurouken crossed at her back, verified f1726 at 0:57.5), performs a **chiburi** (blood-flick) and sheathes them. Cherry petals drift above; a light beam cuts the upper frame. Yuyuko stands small in the left background watching. The huge **Saigyou Ayakashi cherry tree** — one side bare branches, one side in dense bloom ("half-bloomed") — dominates the frame as the camera turns toward Yuyuko (verified f1801 at 1:00).
- **Props:** two katana, sheath, cherry tree, falling petals.
- **Polarity:** **W-on-B**.
- **Transition out:** viewpoint rotates from Youmu to Yuyuko beside the tree.

### Scene 9 — Yuyuko and the cherry petal ★
- **1:04–1:11** | [64.0–71.0 s] | [f 1920–2130]
- **Characters:** Yuyuko Saigyouji
- **Action:** Close-ups of Yuyuko (mob cap with its signature fold, verified f1891/f1936). She opens her **folding fan** and with a wave sends a **single cherry petal** floating off (~1:08); the camera abandons her and follows the petal, zooming in until the petal fills the frame (abstract close-up verified f2011 at 1:07–1:10).
- **Props:** folding fan, single petal.
- **Polarity:** **W-on-B** (petal close-up swallows the frame and flips the field for Scene 10's reveal).
- **Transition out:** the magnified petal morphs into the hull of Komachi's boat.

### Scene 10 — Komachi on the Sanzu River; the screen is cut in half
- **1:11–1:19** | [71.0–79.0 s] | [f 2130–2370]
- **Characters:** Komachi Onozuka
- **Action:** The petal becomes a **white ferry boat** drifting on black; Komachi stands in it with her **scythe over her shoulder** (verified f2161 at 1:12). Close-up of Komachi swinging the scythe across her body (verified f2251 at 1:15). At ~1:17–1:19 the scythe blade sweeps across the screen and **divides the entire frame into one black half and one white half** (wipe in progress verified f2341 at 1:18).
- **Props:** ferry boat, scythe.
- **Polarity:** **W-on-B** → ends as a **50/50 black|white split screen**.
- **Transition out:** Eiki rises at the seam between the two halves.

### Scene 11 — Eiki at the black/white seam ★ (end of verse 2 — lyric "turn black")
- **1:19–1:24.2** | [79.0–84.2 s] | [f 2370–2526]
- **Characters:** Eiki Shiki, Yamaxanadu
- **Action:** On the perfectly split screen (left black / right white), Eiki appears straddling the centerline as a **mirrored dual-polarity silhouette** — white on the black side, black on the white side (verified f2386 at 1:19.5; one of the most reproduced frames of the video). She raises and swings her **Rod of Remorse**, held vertically on the seam (verified f2461 at 1:22). The "make it all black" lyric lands here.
- **Props:** Rod of Remorse, judge's hat.
- **Polarity:** split-screen, both at once.
- **Transition out:** the vertical Rod morphs into Mokou exactly on the chorus-1 downbeat.

### Scene 12 — Mokou's fire (CHORUS 1 begins)
- **1:24.2–1:33** | [84.2–93.0 s] | [f 2526–2790]
- **Characters:** Fujiwara no Mokou
- **Action:** Mokou (very long hair, hair ribbons, suspenders bow) stands on black (verified f2566 at 1:25.5). She conjures a **flame on each open palm** — the fire is rendered with soft gray texture, the only "textured" element so far (one-hand flame verified f2641 at 1:28) — then **claps the two flames together** (~1:30–1:32), and the fire grows.
- **Props:** twin phoenix flames.
- **Polarity:** **W-on-B**.
- **Transition out:** the combined blaze engulfs the whole frame.

### Scene 13 — Keine ×2 inside the blaze; the clockwise spin into the moon
- **1:33–1:39** | [93.0–99.0 s] | [f 2790–2970]
- **Characters:** Keine Kamishirasawa (human form, left) and Hakutaku Keine (horned beast form, right)
- **Action:** Flames fill the screen (verified f2731 at 1:31, two figures emerging at the bottom). Inside the fire, the two Keine forms appear facing each other — human Keine on the left, horned hakutaku Keine on the right — and **clasp hands** at the center (mirrored pair verified f2881 at 1:36). The whole composition then **rotates clockwise**, smearing into a spiral (swirl verified f2941 at 1:38) that resolves into a **full moon**.
- **Props:** flames, hakutaku horns.
- **Polarity:** flame whiteout pushes the field to **B-on-W** momentarily (verified f2806 at 1:33.5), then the pair reads **W-on-B**; the spiral mixes both. Treat 1:33–1:39 as the most polarity-fluid passage of the video.
- **Transition out:** the spiral becomes the moon of Scene 14.

### Scene 14 — Eirin and the full moon
- **1:39–1:45** | [99.0–105.0 s] | [f 2970–3150]
- **Characters:** Eirin Yagokoro
- **Action:** A glowing white **full moon** (soft gray halo — deliberate glow, not a hard silhouette) hangs top-LEFT on black. Eirin stands at the right, head bowed (verified f3001 at 1:40), then **reaches her arm out toward the moon** (verified f3091 at 1:43) and turns away as if renouncing it.
- **Props:** full moon, Eirin's braid/hat.
- **Polarity:** **W-on-B**.
- **Transition out:** camera swings around the moon — it slides to the top-RIGHT — bringing Kaguya in from the left.

### Scene 15 — Kaguya and the moon (end of chorus 1 — lyric "turn white" → whiteout)
- **1:45–1:52.1** | [105.0–112.1 s] | [f 3150–3363]
- **Characters:** Kaguya Houraisan
- **Action:** Mirror composition of Scene 14: moon top-right, Kaguya at the left with her **back turned**, very long straight hair (verified f3166 at 1:45.5). Unable to let go, she too **reaches toward the moon** (profile close-up verified f3241 at 1:48). On the final line of chorus 1 ("if I can change, I'll turn white") the view returns to the moon and the screen **washes out to PURE WHITE** (solid white frame verified f3331 at 1:51).
- **Props:** full moon.
- **Polarity:** **W-on-B** → ends in a full-frame **whiteout** (the famous lyric-synced inversion).
- **Transition out:** the white field becomes the stage of the interlude.

### Scene 16 — Prismriver Ensemble concert ★ (INSTRUMENTAL INTERLUDE begins — documented sync point)
- **1:52.1–1:59** | [112.1–119.0 s] | [f 3363–3570]
- **Characters:** Lyrica Prismriver (keyboard, left), Merlin Prismriver (trumpet, center), Lunasa Prismriver (violin, right)
- **Action:** On the white field, the three poltergeist sisters fade in as black silhouettes and **play the instrumental interlude** (trio verified f3376 at 1:52.5 and f3451 at 1:55 — note the soft **gray floor shadows** under each sister, unique to this scene). Camera tours: full trio → Lunasa (violin) → Merlin (trumpet) → Lyrica (keyboard) (two-shot verified f3511 at 1:57). Lyrica finishes by **waving a hand as if introducing the next act** (~1:58).
- **Props:** keyboard, trumpet, violin & bow; floor shadows.
- **Polarity:** **B-on-W**.
- **Transition out:** Lyrica's introduction gesture cues the rapid-fire face chain.

### Scene 17 — Rapid-fire face chain: Chen → Ran → Tewi ★
- **1:59–2:02** | [119.0–122.0 s] | [f 3570–3660]
- **Characters:** Chen (1:59–2:00), Ran Yakumo (2:00–2:01), Tewi Inaba (2:01–2:02)
- **Action:** Three quick close-up "portrait" shots, one per beat-pair: Chen's face/upper body with cat ears poking through her mob cap, paw raised (verified f3571 at 1:59); Ran's profile head with her tassled hat (verified f3616 at 2:00.5); then a **hard polarity flip** (mid-flip frame verified f3646 at 2:01.5) into Tewi's white rabbit-eared face. This begins the famous second-half cameo barrage.
- **Polarity:** Chen & Ran **B-on-W** → flips to **W-on-B** on Tewi.
- **Transition out:** Tewi's face hands off to Reisen full-body.

### Scene 18 — Reisen's finger-gun beam splits the screen horizontally
- **2:02–2:05** | [122.0–125.0 s] | [f 3660–3750]
- **Characters:** Reisen Udongein Inaba
- **Action:** Reisen (long hair, tall rabbit ears, verified rear view f3691 at 2:03) levels her arm in her trademark **finger-gun pose and fires** (full-body firing stance verified f3736 at 2:04.5). The shot's trace remains as a thin **horizontal white line cutting the whole screen in two** (verified f3766 at 2:05).
- **Props:** finger-gun, beam trace.
- **Polarity:** **W-on-B**.
- **Transition out:** Momiji answers the horizontal cut with a vertical one.

### Scene 19 — Momiji's vertical slash; the screen shatters into leaves
- **2:05–2:07** | [125.0–127.0 s] | [f 3750–3810]
- **Characters:** Momiji Inubashiri (blink-and-miss transition character)
- **Action:** Momiji leaps through and **slashes the screen vertically with her sword**, crossing Reisen's horizontal line; the frame is now quartered. The **four quadrants peel away and turn into giant falling leaves** — a maple leaf and a ginkgo leaf are clearly readable (verified f3796 at 2:06.5, polarity already flipped). LOW CONFIDENCE footnote: one Japanese timestamp list places the **Aki sisters (Shizuha & Minoriko)** among the falling-leaf shapes at ~2:07; no other source corroborates them and the official 36-character lists exclude them — treat as an Easter-egg option, not canon.
- **Props:** sword, four leaf-quadrants.
- **Polarity:** **W-on-B** → flips to **B-on-W** as the quadrants become leaves.
- **Transition out:** the leaves rain down onto Sanae's scene.

### Scene 20 — Sanae sweeps the leaves (VERSE 3 begins)
- **2:07–2:11** | [127.0–131.0 s] | [f 3810–3930]
- **Characters:** Sanae Kochiya
- **Action:** Vocals resume. Tiny Sanae at the bottom of the frame **sweeps the huge falling leaves with a broom** (verified f3826 at 2:07.5 and f3856 at 2:08.5). Close-up: she holds the broom upright and **catches one small maple leaf on her open hand** (verified f3931 at 2:11 — an iconic gentle beat).
- **Props:** broom, falling maple/ginkgo leaves.
- **Polarity:** **B-on-W**.
- **Transition out:** as she watches the caught leaf, Hina bursts in.

### Scene 21 — Hina's spin
- **2:11–2:13** | [131.0–133.0 s] | [f 3930–3990]
- **Characters:** Hina Kagiyama (transition character)
- **Action:** Hina pops out and **pirouettes across the frame**, skirt flared wide by the spin (verified f3976 at 2:12.5), "wiping" the leaves and Sanae off the screen — a literal spin transition (she is the misfortune-collecting goddess always depicted spinning).
- **Props:** flared dress, front ribbon.
- **Polarity:** **B-on-W**.
- **Transition out:** her wipe clears the stage for the Moriya gods.

### Scene 22 — Kanako & Suwako; the gap "switches the TV off"
- **2:13–2:21** | [133.0–141.0 s] | [f 3990–4230]
- **Characters:** Kanako Yasaka, Suwako Moriya
- **Action:** Kanako appears first, tall and stately in her long dress, profile (verified f4021 at 2:14). Suwako then pops up **hat-first** — her broad flat hat rising before her body — and lands in a goofy frog-like arms-out pose (both on screen verified f4081 at 2:16). The two **turn their backs to each other and strike poses** (close-up verified f4171 at 2:19). They exit via what looks like an old **TV switching off** — the frame collapses into a horizontal eye-shaped slit with a white octagon center (verified f4231 at 2:21).
- **Props:** Suwako's hat, Kanako's hair ornament (her onbashira/shimenawa are NOT clearly shown).
- **Polarity:** **B-on-W**.
- **Transition out:** the "TV-off" slit is revealed to be one of Yukari's gaps (sukima) — the eye-shaped boundary rift.

### Scene 23 — Yukari emerges from the gap ★
- **2:21–2:27** | [141.0–147.0 s] | [f 4230–4410]
- **Characters:** Yukari Yakumo
- **Action:** Polarity flips; Yukari rises out of the gap carrying her **parasol** (emergence under a round white canopy verified f4276 at 2:22.5; parasol-from-behind verified f4351 at 2:25). She **opens a folding fan, then snaps it shut** — and someone is hiding behind it.
- **Props:** gap (eye-shaped rift), parasol, folding fan, mob cap.
- **Polarity:** **W-on-B**.
- **Transition out:** the closing fan reveals Tenshi.

### Scene 24 — Tenshi's swagger; the face-off (end of verse 4 — lyric "turn black")
- **2:27–2:35** | [147.0–155.0 s] | [f 4410–4650]
- **Characters:** Tenshi Hinanawi, Yukari Yakumo
- **Action:** Tenshi, revealed from behind the fan, plants her hands on her hips in a full-body cocky pose under a diagonal **spotlight beam** from the corner (verified f4426 at 2:27.5 — the "perfectly captured Tenshi's personality" moment). She gestures grandly, flicking her long hair, holding up a small object (her peach / keystone) (verified f4501 at 2:30, f4561 at 2:32). Quick alternating shots of Yukari and Tenshi (~2:32–2:34) end with the two **facing each other in profile**, noses almost touching (lean-in verified f4621 at 2:34).
- **Props:** hat with peaches, spotlight beam, fan.
- **Polarity:** **W-on-B**.
- **Transition out:** figure-ground flip — the black negative space BETWEEN their two white profiles is suddenly re-read as a solid shape: Aya's wing.

### Scene 25 — Aya the reporter (CHORUS 2 begins)
- **2:35–2:41** | [155.0–161.0 s] | [f 4650–4830]
- **Characters:** Aya Shameimaru
- **Action:** The inter-face negative space becomes a large **feathered crow wing** filling the left frame (verified f4666 at 2:35.5) — polarity is now B-on-W. Pull back to the scene's signature shot: Aya in profile with her **tokin hat**, wings folded behind, **writing in her notebook with a pen** (verified f4741 at 2:38). Done writing, she **tosses the pen** over her shoulder — the pen tumbles alone across the white frame (verified f4816 at 2:40.5).
- **Props:** crow wings, tokin hat, notebook, pen.
- **Polarity:** **B-on-W**.
- **Transition out:** the tumbling pen's shaft morphs into Suika's horn.

### Scene 26 — Suika drains the gourd
- **2:41–2:48** | [161.0–168.0 s] | [f 4830–5040]
- **Characters:** Suika Ibuki
- **Action:** The pen becomes one of Suika's **oni horns**. Suika (huge ponytail, chained wrist) hoists her **two-lobed sake gourd** (verified f4861 at 2:42, chain links clearly readable) and drinks with theatrical abandon, free arm flung up (verified f4951 at 2:45). The gourd runs dry: held upside down overhead, it yields only **one last falling drop** (gourd + lone drop verified f5041 at 2:48).
- **Props:** oni horns, chained gourd, the single sake drop.
- **Polarity:** **B-on-W**.
- **Transition out:** the camera follows the falling drop, which becomes Alice seen from above.

### Scene 27 — Alice drops her doll
- **2:48–2:54** | [168.0–174.0 s] | [f 5040–5220]
- **Characters:** Alice Margatroid (+ her Shanghai/Hourai doll)
- **Action:** The drop morphs into a **bird's-eye view of Alice** standing far below, doll in hand (overhead shot verified f5086 at 2:49.5 — the only top-down camera in the video). Cut to profile: Alice (hairband) holds her **doll up on her palm**, regarding it (verified f5161 at 2:52). Then she simply **lets it fall** — the doll tumbles alone through the white frame (verified f5221 at 2:54). (Community-dubbed the "I don't wanna play with you anymore" moment.)
- **Props:** Hourai/Shanghai doll, hairband.
- **Polarity:** **B-on-W**.
- **Transition out:** the falling doll morphs into Nitori.

### Scene 28 — Nitori's chase and dive (end of chorus 2 — lyric "turn white")
- **2:54–3:01** | [174.0–181.0 s] | [f 5220–5430]
- **Characters:** Nitori Kawashiro
- **Action:** The doll becomes Nitori, who hits the ground **running** (dynamic run with ground shadow verified f5251 at 2:55), chasing something; close-up of her **arm reaching out, fingers spread** to grab it (verified f5341 at 2:58). She **dives** headlong (~2:59–3:00); the impact throws up a **fountain of white spray on black** (droplet burst verified f5431 at 3:01) — the polarity inversion lands exactly on the "turn white" lyric and the section seam.
- **Props:** backpack/key silhouette details minimal; splash particles.
- **Polarity:** **B-on-W** → flips to **W-on-B** with the splash.
- **Transition out:** the spray hangs in the air and becomes flower petals.

### Scene 29 — Petals and Yuka's parasol ★ (FINAL CHORUS — key change up, documented sync point)
- **3:01–3:07** | [181.0–187.0 s] | [f 5430–5610]
- **Characters:** Yuka Kazami
- **Action:** The splash droplets morph into **swirling flower petals** filling the black frame (petal field verified f5476 at 3:02.5) precisely on the key change — a sync moment Japanese fans single out. Among the petals stands Yuka in profile under her **open parasol** (verified f5551 at 3:05 — one of the video's most elegant stills). She **closes the parasol** and extends it out to her side (~3:06–3:07).
- **Props:** parasol, petal storm.
- **Polarity:** **W-on-B**.
- **Transition out:** a hand reaches in and takes the extended parasol — which is now a scythe's shaft.

### Scene 30 — Elly takes the scythe (the PC-98 era enters)
- **3:07–3:15** | [187.0–195.0 s] | [f 5610–5850]
- **Characters:** Elly (gatekeeper of Mugenkan, Lotus Land Story stage 3 boss — the boss of the very stage whose theme "Bad Apple!!" arranges; her inclusion is a deliberate nod to the song's origin)
- **Action:** Close-up: the horizontal parasol-turned-**scythe shaft**, Elly's hand grasping it from the right (verified f5641 at 3:08). Elly bends forward over the scythe (verified f5686 at 3:09.5), then poses with it — bonnet-style hat with ribbon readable in profile, long curved blade sweeping the frame (verified f5761 at 3:12). Sources place her 3:09–3:14 (one says 3:13); she is a **white silhouette**.
- **Props:** scythe, bonnet hat.
- **Polarity:** **W-on-B** (brief mixed-polarity morph frames ~3:14, verified f5836).
- **Transition out:** the camera slides down the scythe to its blade tip.

### Scene 31 — The drop from the blade; crown splash
- **3:15–3:19** | [195.0–199.0 s] | [f 5850–5970]
- **Characters:** none (object scene)
- **Action:** From the downward-pointing **scythe tip a single drop ("blood")** gathers and falls (blade + droplet verified f5881 at 3:16). It lands off-screen and erupts into a perfect **milk-crown splash** — a white coronet on black (verified f5941 at 3:18).
- **Props:** scythe tip, drop, crown splash.
- **Polarity:** **W-on-B**.
- **Transition out:** the crown's rising water column stretches upward and becomes PC-98 Reimu.

### Scene 32 — PC-98 Reimu rises
- **3:19–3:23** | [199.0–203.0 s] | [f 5970–6090]
- **Characters:** Reimu Hakurei (PC-98 / old-works design: hair down, broad kimono-style sleeves, no sleeve ruffles)
- **Action:** The water column morphs into old-works Reimu seen from behind, rising with the water (verified f6031 at 3:21). She **lifts her face to the sky** — and above her, someone is hanging.
- **Polarity:** **W-on-B**.
- **Transition out:** camera tilts up to the figure overhead.

### Scene 33 — PC-98 Marisa upside-down; the two reach for each other ★
- **3:23–3:29** | [203.0–209.0 s] | [f 6090–6270]
- **Characters:** Marisa Kirisame (PC-98 design), Reimu Hakurei (PC-98)
- **Action:** Old-works Marisa hangs **upside-down** inside a white vertical column on black — a BLACK silhouette inside the white band, while Reimu remains WHITE on black beside it (dual-polarity composition verified f6106 at 3:23.5). The frame splits into opposite-polarity halves: left white field with black inverted Marisa, right black field with white Reimu looking up (verified f6181 at 3:26). The two **stretch their hands toward each other** across the divide (verified f6241 at 3:28) — black-half and white-half, yin and yang about to close.
- **Polarity:** simultaneous **both** (left B-on-W / right W-on-B) — the video's thesis made literal.
- **Transition out:** as their hands meet, the halves curl into each other.

### Scene 34 — The spinning yin-yang orb ★ (OUTRO begins)
- **3:29–3:34** | [209.0–214.0 s] | [f 6270–6420]
- **Characters:** none (symbol scene)
- **Action:** The composition resolves into a full-frame **yin-yang symbol** (Reimu's iconic yin-yang orb) that **rotates** for several seconds (verified f6301 at 3:30 and f6391 at 3:33). The two dots of the symbol are the seeds of the final two shots.
- **Polarity:** both at once (the symbol IS the polarity system).
- **Transition out:** the black region's white dot becomes Marisa; the white region's black dot becomes Reimu.

### Scene 35 — Final shots: Marisa ascends, Reimu and the apple; zoom to black ★ (loop point)
- **3:34–3:39** | [214.0–219.0 s] | [f 6420–6569]
- **Characters:** Marisa Kirisame, then Reimu Hakurei
- **Action:** In the black half, **white Marisa rides her broom up and away into the sky** (verified f6451 at 3:35). In the white half, **black Reimu stands holding the apple**, gazing forward (verified f6511 at 3:37; the apple reads as the round shape at her side — in the loop it falls into her hands). The camera **zooms into Reimu's black silhouette until it fills the frame**; the final frames are SOLID BLACK (verified f6556 at 3:38.5) — identical to frame 0, closing the loop. LOW CONFIDENCE detail: whether the final pair use the modern or PC-98 designs is debated (the closing Reimu has hair down and no sleeve ruffles, unlike the opening Reimu; one analysis calls them the modern pair, another reads the design shift as deliberate old-works styling). Recreate as: Reimu with hair down, no sleeve ruffles.
- **Props:** broom, apple.
- **Polarity:** split (Marisa W-on-B / Reimu B-on-W) → ends **solid black**.
- **Transition out:** loops to Scene 1.

---

## Summary table

| # | Time | Frames @30fps | Characters | One-line description | Polarity |
|---|------|---------------|------------|----------------------|----------|
| 1 | 0:00–0:04 | 0–120 | Reimu | Black screen zooms out to reveal Reimu (loop start) | black → B-on-W |
| 2 | 0:04–0:15 | 120–450 | Reimu | Dances with apple, near-bite at 0:08, tosses it skyward ★ | B-on-W |
| 3 | 0:15–0:28.5 | 450–855 | Marisa | Catches apple on broom, starfield flight past SDM, drops core ★ | W-on-B |
| 4 | 0:28.5–0:36 | 855–1080 | Patchouli | Core morphs into Patchouli; dance; raised wagging finger (verse 1) | B-on-W |
| 5 | 0:36–0:42.5 | 1080–1275 | Remilia | Finger→Remilia; bat wings; drops teacup | B-on-W |
| 6 | 0:42.5–0:50 | 1275–1500 | Sakuya | Cup shatters (flip); shard→twirl ("not Rumia"); knife throw | W-on-B |
| 7 | 0:50–0:57 | 1500–1710 | Flandre | Knife→crystal wing; hands out; mid-scene inversion + grin; blade "slice" ★ | W-on-B → B-on-W |
| 8 | 0:57–1:04 | 1710–1920 | Youmu, Yuyuko (bg) | Chiburi + sheathe under half-blooming Saigyou Ayakashi (verse 2) | W-on-B |
| 9 | 1:04–1:11 | 1920–2130 | Yuyuko | Fan wave sends single petal; camera follows petal ★ | W-on-B |
| 10 | 1:11–1:19 | 2130–2370 | Komachi | Petal→Sanzu ferry; scythe wipe halves the screen | W-on-B → split |
| 11 | 1:19–1:24.2 | 2370–2526 | Eiki | Mirrored dual-polarity judge at the seam; Rod of Remorse ★ ("turn black") | split |
| 12 | 1:24.2–1:33 | 2526–2790 | Mokou | Rod→Mokou; twin palm flames combined (chorus 1) | W-on-B |
| 13 | 1:33–1:39 | 2790–2970 | Keine ×2 | Human & hakutaku Keine clasp hands in fire; clockwise spin → moon | mixed |
| 14 | 1:39–1:45 | 2970–3150 | Eirin | Reaches for glowing moon (top-left), turns away | W-on-B |
| 15 | 1:45–1:52.1 | 3150–3363 | Kaguya | Back turned, reaches for moon (top-right); whiteout on "turn white" | W-on-B → white |
| 16 | 1:52.1–1:59 | 3363–3570 | Prismriver ×3 | Interlude concert: Lyrica/Merlin/Lunasa, floor shadows; Lyrica's wave ★ | B-on-W |
| 17 | 1:59–2:02 | 3570–3660 | Chen, Ran, Tewi | One-beat portrait chain ★ (flip on Tewi) | B-on-W → W-on-B |
| 18 | 2:02–2:05 | 3660–3750 | Reisen | Finger-gun shot; beam trace splits screen horizontally | W-on-B |
| 19 | 2:05–2:07 | 3750–3810 | Momiji (+Aki sisters?) | Vertical sword slash; quadrants become falling leaves (flip) | W-on-B → B-on-W |
| 20 | 2:07–2:11 | 3810–3930 | Sanae | Sweeps giant leaves; catches one on her palm (verse 3) | B-on-W |
| 21 | 2:11–2:13 | 3930–3990 | Hina | Pirouette wipe across the frame | B-on-W |
| 22 | 2:13–2:21 | 3990–4230 | Kanako, Suwako | Suwako pops up hat-first; back-to-back pose; "TV-off" gap exit | B-on-W |
| 23 | 2:21–2:27 | 4230–4410 | Yukari | Emerges from gap with parasol; fan open/shut ★ | W-on-B |
| 24 | 2:27–2:35 | 4410–4650 | Tenshi, Yukari | Spotlit swagger; alternating shots; profile face-off ("turn black") | W-on-B |
| 25 | 2:35–2:41 | 4650–4830 | Aya | Negative space→crow wing; writes article; tosses pen (chorus 2) | B-on-W |
| 26 | 2:41–2:48 | 4830–5040 | Suika | Pen→horn; drains chained gourd; last drop falls | B-on-W |
| 27 | 2:48–2:54 | 5040–5220 | Alice | Drop→overhead Alice; holds doll up; lets it fall | B-on-W |
| 28 | 2:54–3:01 | 5220–5430 | Nitori | Doll→Nitori; run, reach, dive; white splash ("turn white") | B-on-W → W-on-B |
| 29 | 3:01–3:07 | 5430–5610 | Yuka | Splash→petal storm on key change; parasol close & extend ★ | W-on-B |
| 30 | 3:07–3:15 | 5610–5850 | Elly | Parasol→scythe; Elly takes it and poses (PC-98 era begins) | W-on-B |
| 31 | 3:15–3:19 | 5850–5970 | — | Drop falls from blade tip; crown splash | W-on-B |
| 32 | 3:19–3:23 | 5970–6090 | PC-98 Reimu | Water column→old-works Reimu; looks up | W-on-B |
| 33 | 3:23–3:29 | 6090–6270 | PC-98 Marisa, PC-98 Reimu | Upside-down Marisa; opposite-polarity halves; hands reach ★ | both |
| 34 | 3:29–3:34 | 6270–6420 | — | Full-frame spinning yin-yang orb ★ | both |
| 35 | 3:34–3:39 | 6420–6569 | Marisa, Reimu | Marisa flies up (black half); Reimu + apple (white half); zoom to black ★ | split → black |

Coverage check: scenes 1–35 are contiguous, 0:00.0 → 3:39.0 (frames 0–6569), no gaps.

---

## Sources & confidence

### Sources actually used
1. **NamuWiki — "Bad Apple!! feat. nomico / PV 등장 순서"** (order-of-appearance page; fetched raw): the complete 31-entry / 36-character scene narrative used as the action backbone (every morph/prop description), plus production trivia (storyboard by Μμ; "spinning Rumia" debunked as Sakuya via the published storyboard; Suika hot-spring scene cut; Prismriver scene = interlude start). https://namu.wiki/w/Bad%20Apple!!%20feat.%20nomico/PV%20%EB%93%B1%EC%9E%A5%20%EC%88%9C%EC%84%9C
2. **YouTube comment timestamp lists on the original reprint (FtutLA63Cp8)** — five independent full lists (three English, one Japanese, one annotated-by-game), retrieved via the YouTube API. Mutual agreement within ±2 s for all 36 appearances. Also confirmed `lengthSeconds: 219`.
3. **SpaceHey blog "I overanalyzed the Bad Apple AMV"** — independent anchors: Reimu 0:08, Momiji 2:05, Hina 2:12, Elly 3:13, closing Reimu 3:27; opening-vs-closing Reimu design differences (hair up + sleeve ruffles vs hair down, none).
4. **TV Tropes (Music/BadApple)** — opening (black screen zooms out to Reimu, apple toss, Marisa catch) and ending (yin-yang dots → Marisa flying away / apple falling into Reimu's hands → zoom-in to solid black); statement that the video is entirely black/white silhouettes on opposite backgrounds.
5. **Frame-level verification — `bleov/bad-apple-frames` GitHub repo** (all 6572 frames of the original at 480×360, 30 fps): **97 frames downloaded and visually inspected** (kept in `_ref_frames/`). This is the basis for every "verified fNNNN" note and all polarity calls.
6. **Touhou Wiki (en.touhouwiki.net/wiki/Bad_Apple!!), Wikipedia, NicoNicoPedia (dic.nicovideo.jp/v/sm8628149), note.com analysis (genial_hebe9762)** — metadata (upload date, creator, view counts), the game-chronology casting principle, the deliberate Reimu beginning/end loop, characters limited to pre-Subterranean-Animism.
7. **Musical grid:** 138 BPM section math anchored to the verified events (verse 1 = Patchouli 0:29, verse 2 = Youmu 0:57 ["夢見てる" pun], chorus 1 = Mokou 1:25, interlude = Prismriver 1:52, verse 3 = Sanae 2:07, chorus 2 = Aya 2:35, key change = Yuka petals 3:01 [confirmed by a Japanese comment singling out the 転調], outro = yin-yang 3:29). All eight derived boundaries coincide with sourced scene starts.

### Confidence by section
- **Character order (all 36):** VERY HIGH — 6+ independent sources in full agreement; no omissions or inventions.
- **Scene start timestamps:** HIGH — consensus of 5 timestamp lists (±1–2 s spread; where they disagreed, the range is absorbed into scene boundaries) and ~30 boundaries directly confirmed by frame inspection.
- **Section (verse/chorus) boundaries:** HIGH — BPM-grid derived, but every boundary independently confirmed by an on-screen event; treat as ±0.5 s.
- **Polarity:** HIGH at scene level (every scene's dominant polarity read directly from frames). MEDIUM for the exact frame of each flip — flips were bracketed between sampled frames (typically a 30–45-frame window); animators should place flips exactly on the morph/accent within the listed transition windows.
- **LOW CONFIDENCE items (explicitly flagged in scenes):** (a) Aki sisters cameo in the 2:06–2:08 leaf shapes — single-source, contradicts the canonical 36-count; (b) modern-vs-PC-98 design of the final Marisa/Reimu (Scene 35) — sources conflict; recreate per the visual description given; (c) micro-actions at 2:16–2:20 (Kanako/Suwako posing details between verified frames) and 2:32–2:34 (exact Yukari/Tenshi shot alternation pattern) — narrative from NamuWiki + one comment list, not frame-bracketed shot-by-shot; (d) the precise moment the apple enters Reimu's hands in Scene 1 (inferred from the documented loop + TV Tropes ending description).
