import tkinter as tk
import random
import time
import threading
from tkinter import messagebox


# Define the lists of settings

player_settings = {

    "Starting sanity": {"values": [0, 25, 50, 75, 100]},

    "Sanity Pill restoration": {"values": [0, 5, 10, 20, 25, 30, 35, 40, 45, 50, 75, 100]},

    "Sanity drain speed increased": {"values": [50, 100, 150, 200]},

    "Sprinting": {"values": ["on", "off", "infinite"]},

    "Player speed": {"values": [50, 75, 100, 125, 150]},

    "Flashlights": {"values": ["on", "off"]}

}



ghost_settings = {

    "Ghost speed": {"values": [50, 75, 100, 125, 150]},

    "Roaming frequency": {"values": ["low", "medium", "high"]},

    "Changing of favourite Room": {"values": ["none", "low", "medium", "high"]},

    "Interaction amount": {"values": ["low", "medium", "high"]},

    "Event frequency": {"values": ["low", "medium", "high"]},

    "Grace period": {"values": [0, 1, 2, 3, 4, 5]},

    "Hunt duration": {"values": ["low", "medium", "high"]},

    "Kills extending hunts on": {"values": ["off", "low", "medium", "high"]},

    "Number of evidence given": {"values": [0, 1, 2, 3]},

    "Fingerprint chance": {"values": [25, 50, 75, 100]},

    "Fingerprint duration": {"values": [15, 30, 60, 90, 120, 180, "infinite"]}

}



contract_settings = {

    "Setup time": {"values": [0, 30, 60, 120, 180, 240, 300]},

    "Weather": {"values": ["Random", "Light Rain", "Heavy Rain", "Snow", "Windy", "Clear", "Fog", "Sunrise"]},

    "Doors starting open": {"values": ["none", "low", "medium", "high"]},

    "Number of hiding places": {"values": ["none", "low", "medium", "high", "Very High"]},

    "Sanity monitor": {"values": ["on", "off"]},

    "Activity monitor": {"values": ["on", "off"]},

    "Fuse box": {"values": ["Broken", "on", "off"]},

    "Cursed Possessions": {"values": [0, 1, 2, 3, 4, 5, 6, 7], 

                                    "items": ["Monkey Paw", "Trot Cards", "Voodoo Doll", "Music Box", "Ouija Board", "Summoning Circle", "Haunted Mirror",]}

}



random_difficulty = ["\nAmateur",

                     "\nIntermediate",

                     "\nProfessional",

                     "\nNightmare",

                     "\nInsanity",

                     "\nLights Off Challenge: \n-Flashlights: Off  \n-Fuse Box: Broken",

                     "\nOne Type Of Evidence Run: \n-Ghost Evidence Types: One  \n-Fingerprint chance: 25 \n-Fingerprint duration:15",

                     "\nSpeed Runner Challenge: \n-Sprint Duration: Infinite \n-Player Speed: 150 \n-Ghost Speed: 150",

                     "\nNo Sprinting: \n-Sprinting: Off \n-Player Speed: Normal",

                     "\nAngel Numbers: \n-Everything that can be three should be set to three \n-Any Things that can't be three should be the third option",

                     "\nThis House Is Cursed: \n-Turn on all cursed objects \n-Fuse Box: Broken \n-Doors starting open: High",

                     "\n20/20/20 Mode: \n-All settings should have green arrows at the max next to them \n-There can not be any red arrows",

                     "\nRainy-Day: \n-Weather: Heavy rain \n-Sprint Recharge: 6 \n-Player Speed: 75 \n-Flashlight: Off \n-Fuse Box: Broken \n-Fingerprint Duration: 15",

                     "\nIndecisive Ghost: \n-Roaming Frequency: High \n-Changing Favorite Room: High",

                     "\nNowhere To Hide: \n-Hiding Spaces: None \n-Grace Periods: 0 \n-Hunt Duration: High \n-Kills Extend Hunts: High",

                     "\nThe Insanity Challenge: \n-Starting Sanity: 0 \n-Sanity Pills Restore: 0 \n-Sanity Drain: 2",

                     "\nNo Evidence Run: \n-All evidence turned off"]

                     

class GhostTester:

    def __init__(self, master):

        self.master = master

        master.title("Ghost Tester")

        self.ghost_types = [

            "Banshee",

            "Demon",

            "Deogen",

            "Goryo",

            "Hantu",

            "Jinn",

            "Mare",

            "Moroi",

            "Myling",

            "Obake",

            "Oni",

            "Onryo",

            "Phantom",

            "Poltergeist",

            "Raiju",

            "Revenant",

            "Shade",

            "Spirit",

            "Thaye",

            "The Mimic",

            "The Twins",

            "Wraith",

            "Yokai",

            "Yurei",

        ]

        
        self.ghost_info = {

            "Banshee": "Evidence: Fingerprints | Ghost Orbs | DOTs \n\nPrefers singing ghost events. \n\nWill target a single player (ignoring others while hunting). \n\nFrequently wanders away from favourite room to target; use motion sensors to check. Seeing ghost activity far away from the favourite room (especially on larger maps) could indicate a Phantom / Wraith/ Banshee / The Twins, but this will be more common with Banshee. \n\nBanshees scream through the Parabolic Microphone (33% to replace a whisper). \n\nHunts based solely on target's sanity (even if outside); no hunts despite low average sanity but with one high-sanity player may indicate them as target, and vice versa. \n\nIf target is outside building/investigation area, will hunt normally (i.e. can chase and kill other players).",

            "Demon": "Evidence: Fingerprints | Ghost Writing | Freezing Temperatures \n\nTest: If it hunts before 25 seconds, it is a Demon. Hunting 25 seconds or later does not exclude Demon \n\nTest: If it hunts within 60 - 89 seconds, it is probably a Demon. Hunting only after 90 seconds does not exclude Demon \n\nMinimum hunt cooldown of 20 seconds, instead of standard 25 seconds (excluding cursed hunts) \n\nHunt sanity threshold of 70%, with rare chance to hunt at any sanity Smudging prevents regular hunts for next 60 seconds, instead of standard 90 seconds \n\nRarely, the smudge may not apply successfully (either out of range or otherwise bugged); this may lead to misjudgements. Hunting before 60 seconds means that the ghost was not cleansed \n\nEffective crucifix range of 5 meters, instead of standard 3 meters \n\nHaving a lazily placed crucifix burn when the ghost would normally not have used it may indicate a Demon, though ghosts could happen to wander away from their room into the crucifix's range \n\nA crucifix being used while still on the van wall on 42 Edgefield Road is almost certainly a Demon (usually in the garage or master bedroom) ",

            "Deogen": "Evidence: Spirit Box | Ghost Writing | DOTs \n\nGuaranteed Evidence: Spirit Box \n\nTest: During a hunt, stay near or in a hiding spot, and listen for the ghost running quickly to a player and slowing down massively as it approaches \n\nThe Thaye has a similar speed to a Deogen far away when young; prepare a smudge stick in case it is not a Deogen \n\nHunt sanity threshold of 40% \n\nIncreased chance to interact with D.O.T.S Projector and Ghost Writing Book \n\nAlways knows the location of all players, and speed is based on distance to currently targeted player (3 m/s when further than 6 metres, 0.4 m/s when closer than 2.5 metres) \n\nWhen using the Spirit Box within 1 metre of the Deogen, 33% chance per question to produce a bull-like breathing sound instead of a regular response \n\nSet up motion sensors to accurately track the ghost's location, and use the spirit box near it. \n\nGhost event/hunt vocalisations do not count.",

            "Goryo": "Evidence: EMF 5 | Fingerprints | DOTs \n\nGuaranteed Evidence: DOTs \n\nD.O.T.S Projector silhouette only visible through a video camera, and while no players are in the ghost's current room \n\nSeeing the silhouette without a video camera eliminates Goryo \n\nNot based on where the D.O.T.S Projector or favourite room is; if you are in the favourite room and the Goryo roams out, you could still see the silhouette \n\nGhost events and hunts are not affected by this ability \n\nWill never change favourite room; the ghost doing so (having confirmed by Haunted Mirror or other means) eliminates Goryo \n\nNever changing favourite room could be (but not definitely) a Goryo; the larger the room is, the less likely the ghost is to change rooms \n\nGoryo Cannot wander far distances; ghost activity being relatively confined to favourite room and immediate vicinity (excluding ghost events and hunts) could indicate a Goryo.",

            "Hantu": "Evidence: Fingerprints | Ghost Orbs | Freezing Temperatures \n\nGuaranteed Evidence: Freezing Temperatures \n\nTest: Listen for hunt speed; if it is very fast in a cold room (favourite room is usually but not always cold) but slower in warm rooms, then it is probably a Hantu. Alternatively, turn the fuse box off, then listen for its footsteps over several hunts \n\nSpeed based on room's current temperature and will not speed up on line-of-sight: slowest at 1.4 m/s when above 15°C (59°F), fastest at 2.7 m/s below 0°C (32°F) \n\n Will never turn on the fuse box; a ghost doing so eliminates Hantu \n\nWill emit freezing breath during a hunt if fuse box is turned off \n\nTwice as likely to turn off the fuse box relative to other ghosts",

            "Jinn": "Evidence: EMF 5 | Fingerprints | Freezing Temperatures \n\nTest: Place EMF Reader on fuse box. If it rings without anything else happening, then it is likely the Jinn's ability. Note that the fuse box turning on and off/its door closing is not indicative. Depending on where EMF is placed, it could also be another ghost using its own ability while standing besides the fuse box \n\nTest: Stand at the end of a long hallway or room, then wait for ghost to appear at the other end. If its speed increases instantly and not over a period of time, then it is a Jinn \n\nSpeed fixed at 2.5 m/s if three conditions are met: fuse box is on, Jinn is chasing player, and the player is further than 3 metres. Otherwise, chases at standard ghost speed \n\nUnlike Revenant, has normal speed when not chasing a player, and ability is not based on hearing player or detecting electronics \n\nOccasionally, decreases sanity of all players in same room or within 3 metres by 25%, giving an EMF reading at the fuse box \n\nWill never turn off fuse box, but can still overload if too many lights are turned on (set limit based on map size) \n\nFuse box never being turned off after a long time could mean (but not definitely) a Jinn",

            "Mare": "Evidence: Spirit Box | Ghost Orbs | Ghost Writing \n\nWill never turn individual lights on; a ghost doing so eliminates Mare \n\nThis includes televisions and computers, but not car alarm/radio \n\nHas a chance of turning the lights off immediately if a player turns it on nearby, giving an EMF 2 reading \n\nNote that any ghost can do this by chance \n\n10-second cooldown on a per-light basis, if you turn the light on before the cooldown is over it will restart \n\nMare must be within 4 metres of the light to potentially trigger ability \n\nHunt sanity threshold: 40% if lights on, 60% if off \nApplies even if fuse box is off/broken \n\nDecreases interactions if room is lit \n\nMore likely to perform light-shattering ghost events \n\nLess likely to roam into a lit room; having the ghost roam frequently when lights are on could indicate a Mare",

            "Moroi": "Evidence: Spirit Box | Ghost Writing | Freezing Temperatures \n\nGuaranteed Evidence: Spirit Box \n\n Test: Smudging during a hunt ‘blinds’ the Moroi for 12 seconds instead of 6. If the ghost continues to wander aimlessly 6 seconds after the smudge effect hits, then it is probably a Moroi,\n\nTest: If sanity monitor is broken, after receiving a spirit box/paramic response, the questioner can consume sanity pills to reach maximum sanity, then hold a lit candle going back in, then receive another spirit box/paramic response, wait about 30 seconds, then finally return to the van again and attempt to eat another sanity pill. If the player can eat a sanity pill, then it is probably a Moroi. \n\nCurses a player if Spirit Box response obtained or whisper through Parabolic Microphone heard. This doubles their sanity drain, and lights will not stop sanity drain. Curse temporarily pauses when player is outside the house, and Sanity Pills remove the curse for a player. \n\nTake note of sanity at time of receiving spirit box/paramic response and a few minutes after; if one person's sanity drops noticeably quicker than others, then it could be due to the curse \n\nSanity can drain in other ways, such as ghost events or abilities; try to eliminate these possibilities \n\nSpeed based on current average sanity (1.5 m/s base speed above 45% sanity, 2.25 m/s at ~0% sanity). Will also increase speed in line-of-sight \n\nIf base speed increases over several hunts, then it could be a Moroi \n\nEnsure that it is not a Hantu by keeping the fuse box on (if possible)", 

            "Myling": "Evidence: EMF 5 | Fingerprints | Ghost Writing \n\nTest: Go to a hiding spot and place an active electronic on the ground. If the ghost's footsteps/vocalisations are audible only when the specified electronic starts flickering (within 10 metres of ghost), then it is probably a Myling \n\nFootsteps and vocalisations can only be heard within 12 metres (instead of 20 metres) \n\nNote that the Raiju interferes with electronics from further (15 metres) \n\nThis test is not reliable if the ghost is on a different floor, since electronics will not flicker \n\nSome vocalisations can be very soft; try listening for footsteps in this case \n\nNote the audible range being slightly larger than the interference range. Some specific audio setups may allow you to hear the ghost before electronics flicker \n\nIncreased frequency of paranormal sounds when listening through parabolic microphone",

            "Obake": "Evidence: EMF 5 | Fingerprints | Ghost Orbs \n\nGuaranteed Evidence: Fingerprints  \n\n16.7% chance to leave unique fingerprint pattern: Six-fingered handprints instead of five, two fingerprints on light switches instead of one, and five fingerprints on keyboards and Prison cell block gates instead of four \n\nDuring a hunt, 1 in 15 (~6.67%) chance for the Obake to appear as a different ghost model every time it flickers visible \n\nWill return to normal on next flicker \n\nGuaranteed to happen at least once per hunt \n\n25% chance to not leave fingerprints when interacting with a valid surface (for standard difficulties). If you see it leave a fingerprint once but not on another time, then it is probably an Obake \n\nOccasional ability to halve the remaining duration of existing fingerprints on the map",

            "Oni": "Evidence: EMF 5 | Freezing Temperatures | DOTs \n\nWill never cause 'airball' ghost event (airball chases a player, before disappearing with a hiss); a ghost doing so eliminates Oni \n\nWill still hiss if it manifests to chase a player and disappears due to colliding with the player \n\nSome maps have a larger mist that will fly out of the building in a straight line and disappear. Seeing this also eliminates Oni \n\nWill be visible for a longer period when flickering during hunts; seeing a ghost that doesn't disappear as often as other ghosts during a hunt makes it probably an Oni \n\nDuring ghost events, more likely to use its full ghost model instead of a shadow or translucent form \n\nDouble sanity drain during a ghost event if it collides with a player (20% instead of 10%)",

            "Onryo": "Evidence: Spirit Box | Ghost Orbs | Freezing Temperatures \n\nTest: At high sanity, place a crucifix down, then a lit candle directly on top of it. If it uses the crucifix without blowing out the candle, then it is not an Onryo. Alternatively, let it blow out the candle 3 times; if it hunts on the third blowout, then it is likely an Onryo (try to eliminate Demon as a possibility) \n\nTest: Spread out multiple lit candles in the favourite room and nearby (as desired), then keep them continously lit while average sanity is low. If the ghost refuses to hunt, it could be (but not definitely) an Onryo \n\nThe Shade will not hunt if at least one player is in its room. Try to eliminate this ghost \n\nIf attempts to hunt within 4 metres of a flame (candle, lighter, Maple Lodge Campsite campfire), it will blow out the flame instead \n\nIn addition, prioritises blowing out a flame instead of using a crucifix \n\nConfusingly, every third flame that the Onryo blows out will also cause it to hunt \n\nCan still be prevented by normal methods (crucifix/smudge/another lit flame) \n\nHunt sanity threshold of 60%",

            "Phantom": "Evidence: Spirit Box | Fingerprints | DOTs \n\nTaking a photo of a Phantom will make it instantly and temporarily disappear for that specific instance that it appears \n\nWill not end the ghost event or hunt, but in ghost events, electronics will no longer flicker \n\nGhost photo will be labelled but the ghost will not be visible, and there will be no interference. Note that this can occur for any ghost if the photo is taken exactly at the end of the ghost event/hunt, and the photo can also have no interefence if taken from another floor \n\nBest to check if the ghost event continues (listen for ghost vocalisations) \n\nDuring a hunt, flashes visible every 1 to 2 seconds as opposed to every 0.3 to 1 seconds for other ghosts. The ghost being invisible for long periods could indicate a Phantom \n\nWill occasionally walk (invisibly) to a random player outside of hunts/ghost events; seeing ghost activity far away from the favourite room (especially on larger maps) could indicate a Phantom/Wraith/Banshee/The Twins",

            "Poltergeist": "Evidence: Spirit Box | Fingerprints | Ghost Writing n\n\Test: During a hunt it has a 100% chance to throw an item in its path every 0.5 seconds, instead of 50% with all other ghosts n\n\Test: Create several piles of objects in and near the favourite room (try not to stack items), then see if the ghost throws multiple objects at once. \n\nHas an ability to throw all nearby items at the same time. \ \n\nNoticing a considerable number of items being thrown around (much more than usual) after the hunt could indicate a Poltergeist \n\nTends to throw objects more frequently than other ghosts in general \n\nNote that all ghosts cannot throw items if the room they are currently standing in is lit, though the multithrow ability overrides this \n\nCan throw items much further than other ghosts (up to twice as far). Noticing items being ‘shot’ across the room (i.e, a dining utensil found across the living room from the nearby dining room) could indicate Poltergeist",

            "Raiju": "Evidence: EMF 5 | Ghost Orb | DOTs \n\nFixed speed of 2.5 m/s if there is at least one piece of active electronic equipment nearby (within 6-10 metres depending on map size) \n\nStandard ghost speed if not near these equipment \n\nElectronic interference range during ghost events or hunts is 15 metres, compared to the standard 10 metres \n\nLike other ghosts, does not interfere with electronics on a different floor \n\nDetection range is still 7.5 metres like other ghosts \n\nGetting EMF Level 5 and Ghost Orbs on difficulties with 2 evidences (e.g. Nightmare) confirms Raiju, since the only other ghost that has these two evidences is the Obake, which has Fingerprints as a guaranteed evidence \n\nHunt sanity threshold is 65% if at least one piece of active electronic equipment nearby, otherwise 50%",

            "Revenant": "Evidence: Ghost Orb | Ghost Writing | Freezing Temperatures \n\nDuring a hunt, moves at 1 m/s if no player detected. If a player is detected or when moving to last known player location, moves at 3 m/s. After arriving at last known location, it will decrease its speed by 0.75 m/s² until it reaches 1 m/s (over ~2.7 seconds)",
            
            "Shade": "Evidence: EMF 5 | Ghost Writing | Freezing Temperatures \n\n Cannot interact with items (except Ghost Writing) or hunt if at least one player is in the same room as the ghost, regardless of average sanity \n\nCan still happen if it wanders into a room with no players \n\nNote that turning lights on in ghost's current room will prevent EMF 3 interactions (throws) but not EMF 2 interactions (door touch, window knock, etc.) \n\nIf summoned by a Summoning Circle, a Music Box, or a Monkey Paw, has a chance of appearing as a shadow instead of a full form; will return to normal upon hunt starting \n\nAbove 50% average sanity, increasing sanity means decreasing chance of ghost events; a ghost event at very high sanity may mean that a Shade is unlikely (but not impossible) \n\nHunt sanity threshold of 35% \n\nIncreased chance of airball ghost events instead of manifesting. If it does manifest, has increased chance of using shadow model instead of full/translucent form",

            "Spirit": "Evidence: EMF5 | Spirit Box | Ghost Writing. \n\nTest: Get sanity as low as possible, then cleanse the ghost and wait. If it hunts before 180 seconds is up, then it is not a Spirit. \n\nCleansing prevents hunts for 180 seconds instead of 90 seconds \n\nHunting only after 180 seconds may indicate (though not definitely) a Spirit Rarely. \n\nthe smudge may not apply successfully (either out of range or otherwise bugged); this may lead to misjudgements. \n\nHunting before 60 seconds means that the ghost was not cleansed.",

            "Thaye": "Evidence: Ghost Orbs | Ghost Writing | DOTS \n\nHas ‘age’ parameter, where it will age the more time players spend in the same room as the Thaye. Speed is based on age and does not speed up with line-of-sight; is fast at youngest (2.7 m/s at age 0) and slow when old (1 m/s at age 10) \n\nGetting Ghost Writing and D.O.T.S Projector on difficulties with 2 evidences (e.g. Nightmare) confirms Thaye, since the only other ghost that has these two evidences is the Deogen, which has Spirit Box as guaranteed evidence \n\nAge parameter also affects activity and hunt sanity threshold: \n\nTwice as active compared to normal ghost when youngest, half as active compared to normal ghost when oldest \n\n75% hunt sanity threshold at youngest, 15% at oldest \n\nMore likely to interact with the D.O.T.S Projector and Ghost Writing Book",  

            "The Mimic": "Evidence: Spirit Box | Fingerprints | Freezing Temperatures \n\nGuaranteed Evidence: Ghost Orbs\n\nGhost Orbs as ‘secondary evidence’ or ability in addition to main evidences; this means that they will always be present, even on 0-evidence difficulties \nFor example, you can obtain Fingerprints, Spirit Box, and Ghost Orbs on Nightmare difficulty. If the difficulty gives less than 3 evidence, check for presence of additional evidence \n\nIf you get EMF 5, Ghost Writing, or D.O.T.S Projector, you can safely eliminate The Mimic since it cannot mimic evidence \n\nRandomly mimics another ghost, along with all its abilities and behaviour, such as 6-fingered handprints when mimicking Obake. Will change every 30 seconds to 2 minutes, but will not change during hunts \n\nLook for the ghost demonstrating two completely different traits (such as noticing the ghost flickering slower like a Phantom during a hunt, when it was not doing so earlier)",

            "The Twins": "Evidence: EMF 5 | Spirit Box | Freezing Temperatures \n\nIs simply one ghost with two interaction ranges; the first within 3 metres and the second within 16 metres. Occasionally, will interact with the environment almost simultaneously (within 1 second) using these two ranges; noticing two interactions occurring in very quick succession at two separate locations, especially several times, can indicate The Twins \n\nUse EMF readers and see if both readings stop within less than 1 second of each other. \n\nAll ghosts can interact with items within about 2 seconds in between, while cursed possessions can also cause near-simultaneous interactions (e.g. repeatedly using Voodoo Doll) \n\nInteractions for all ghosts happen in a radius confined to the same floor; they can interact through walls in an adjacent room \n\nDepending on where hunt starts, has slightly different base speed; 1.5 m/s if starts from where the ghost actually is, and 1.9 m/s if it starts from the location where the large-range interaction occurred \n\nBecause it is one ghost with two interaction ranges, you could misidentify where the ghost actually is; noticing a single interaction in one area, but then realising that the ghost was never there (e.g. absence of low temperatures/another room is of low temperatures) could indicate The Twins. Other indicators of ghost presence include motion sensors to track ghost movement, and evidences \n\nLook for items interacted with by the ghost far away from ghost room (e.g. thrown objects, turned-on lights). Seeing ghost activity far away from the favourite room (especially on larger maps) could indicate a The Twins/Phantom/Wraith/Banshee \n\n50% chance to hunt from where the ghost actually is, or from ‘ranged’ interaction \n\nThe ghost hunting far away from the favourite room could indicate The Twins, one of the ghosts mentioned above, or simply a very roamy ghost",

            "Wraith": "Evidence: EMF 5 | Spirit Box | DOTS \n\nTest: During a ghost event, place salt under the ghost. If it doesn't leave an imprint despite walking over, then it is a Wraith. This is best done with stationary ghost events (e.g. singing) \nNote that all ghosts will not 'interact' with salt during hunts \n\nWill never step in salt (will walk over without leaving imprint/UV footsteps). Seeing these eliminates Wraith \n\nSimilarly, if the ghost never steps in salt after a long time, then it is likely (though not definitely) a Wraith \n\nCan teleport to a random player when not hunting/performing ghost events, leaving an EMF 2/5 reading. Seeing ghost activity far away from the favourite room (especially on larger maps) could indicate a Wraith/The Twins/Phantom/Banshee",

            "Yokai": "Evidence: Spirit Box | Ghost Orbs | DOTS \n\nTest: Stand in a room at a suitable distance away from the ghost, hold an electronic equipment (to check if the ghost is within 10 metres), then repeatedly talk/use global chat (since voice detection for normal ghosts is 9 metres as opposed to electronic detection, which is 7.5 metres). If the ghost is nearby with no line-of-sight but does not enter the player's room despite the potential attraction, then it could be a Yokai. Note that the ghost going to the player does not eliminate Yokai, since it could have wandered over by chance \n\n Can only sense player voices/held electronics within 2.5 metres \n\nHunt sanity threshold is 80% if players are talking near the ghost, otherwise 50% \n\nIncreased ghost activity if players are talking near the ghost",

            "Yurei": "Evidence: Ghost Orbs | Freezing Temperatures | DOTS \n\nHas an ability where it will drop the sanity of all players within 7.5 meters of it by 15%, while also closing a door sharply at the same time. Seeing this door close very likely indicates (but not definitely) a Yurei \n\nNote that any ghost can close a door this way; the Yurei simply does it much more often because it is also part of its ability \n\nIf this occurs on an exit door, then it is definitely a Yurei \n\nThis does not count during ghost events or hunts \n\nWill walk back to favourite room and not wander out for 60 seconds when smudged. Place a Motion Sensor at the doorway, then smudge the ghost. If the motion sensor is never set off by the ghost within the next 60 seconds, then the ghost could be a Yurei. This test is not very reliable \nGhost events override this mechanic",
}
        
        self.buttons = []



        for i, ghost_type in enumerate(self.ghost_types):

            button = tk.Button(master, text=ghost_type, command=lambda g=ghost_type: self.button_clicked(g))

            button.grid(row=i // 5, column=i % 5, padx=10, pady=10)

            self.buttons.append(button)
            

    def button_clicked(self, ghost_type):
        self.open_ghost_info(ghost_type)

    def open_ghost_info(self, ghost_type):
        ghost_info_window = tk.Toplevel(self.master)
        ghost_info_window.title(ghost_type)

        ghost_info_label = tk.Label(ghost_info_window, text=f"Information about {ghost_type}:\n\n{self.ghost_info[ghost_type]}", wraplength=300, justify="left")
        ghost_info_label.pack(padx=20, pady=20)

        if ghost_type == "Spirit":
           timer_button = tk.Button(ghost_info_window, text="Start 3-minute timer", command=self.start_timer)
           timer_button.pack(padx=20, pady=20)
        elif ghost_type == "Demon":
             timer_button = tk.Button(ghost_info_window, text="Start 60-second timer", command=self.start_demon_timer)
             timer_button.pack(padx=20, pady=20)


    def start_timer(self):
       def timer():
           time.sleep(180)  # Sleep for 3 minutes (180 seconds)
           tk.messagebox.showinfo("Timer Ended", "The Spirit Smudge timer has finished you might want to RUNNNNNNN!!!!!")

       # Start the timer in a new thread
       timer_thread = threading.Thread(target=timer)
       timer_thread.start()


    def start_demon_timer(self):
        self.master.after(60000, self.demon_timer_ended)  # 60 seconds * 1000 milliseconds

    def demon_timer_ended(self):
        messagebox.showinfo("Timer Ended", "Demon Smudge Timer has finished")
    

class GUI:

    def __init__(self, master):

        self.master = master

        master.title("ProstoPhasma by Prosto Alex")

        

        self.theme = "light"



        # Console output

        self.console = tk.Text(master, height=30, width=95)

        self.console.grid(row=0, column=0, columnspan=3, padx=10, pady=10)  # Update columnspan to 3

        self.console.insert(tk.END, "Select from the buttons random custom mode or random difficulty or quit: \n")



        # Button 1

        self.button1 = tk.Button(master, text="Random Custom Mode", command=self.random_custom_mode_clicked)

        self.button1.grid(row=1, column=0, padx=10, pady=10)



        # Dropdown list

        self.dropdown_value = tk.StringVar(master)

        self.dropdown_value.set("1")

        self.dropdown_options = [str(i) for i in range(1, 26)]

        self.dropdown = tk.OptionMenu(self.master, self.dropdown_value, *self.dropdown_options, command=self.dropdown_selected)  # Add command parameter

        self.dropdown.grid(row=2, column=0, padx=10, pady=10)  # Update grid position to row=2, column=0



        # Button 2

        self.button2 = tk.Button(master, text="Random Difficulty", command=self.random_difficulty_clicked)

        self.button2.grid(row=1, column=1, padx=10, pady=10)



        # Button 4 - Toggle Theme

        self.button4 = tk.Button(master, text="Toggle Theme", command=self.toggle_theme)

        self.button4.grid(row=1, column=2, padx=10, pady=10)



        # Button 3

        self.button3 = tk.Button(master, text="Quit", command=self.quit_program_clicked)

        self.button3.grid(row=2, column=2, padx=10, pady=10)  # Update grid position to row=2, column=2

        

        # Button 5 - Open Ghost Tester

        self.button5 = tk.Button(master, text="Open Ghost Tester", command=self.open_ghost_tester)

        self.button5.grid(row=2, column=1, padx=10, pady=10)



        # Initially hide the dropdown list and the "Generate Settings" button

        self.dropdown.grid_remove()



    def quit_program_clicked(self):

        self.master.destroy()

        

    def open_ghost_tester(self):

        ghost_tester_window = tk.Toplevel(self.master)

        ghost_tester = GhostTester(ghost_tester_window)

        

    def random_difficulty_clicked (self):

        # Clear the console

        self.clear_console()

        # Console output

        self.console.insert(tk.END, "Select from the buttons random custom mode or random difficulty or quit:\n")

        # Pick a random difficulty from the list and print it

        random_difficulty_choice = random.choice(random_difficulty)

        self.console.insert(tk.END, f"\nRandom difficulty selected: \n{random_difficulty_choice}\n")



    def random_custom_mode_clicked(self):

        # Clear the console

        self.clear_console()

        # Console output

        self.console.insert(tk.END, "Select from the buttons random custom mode or random difficulty or quit\n")

        # Show dropdown list

        self.dropdown.grid(row=2, column=0)

        

    def dropdown_selected(self, event=None):

        # Clear the console

        self.clear_console()

        # Console output

        self.console.insert(tk.END, "Select from the buttons random custom mode or random difficulty or quit\n")

        # Get selected value

        selected_value = self.dropdown_value.get()

        # Convert selected value to an integer

        num_settings = int(selected_value)

        # Remove dropdown and update options

        self.dropdown_value.set("1")

        self.dropdown.grid_remove()  # Use grid_remove() instead of pack_forget()

        

  

        # Create a list of all possible settings

        all_settings = []

        all_settings.extend(player_settings.keys())

        all_settings.extend(ghost_settings.keys())

        all_settings.extend(contract_settings.keys())



        # Pick a random selection of settings

        selected_settings = random.sample(list(player_settings.keys()) + list(ghost_settings.keys()) + list(contract_settings.keys()), k=num_settings)



        # Print the selected settings

        self.console.insert(tk.END, "\nRandom settings selected:\n")

        for setting in selected_settings:

            if setting in player_settings:

                values = player_settings[setting]['values']

                random.shuffle(values)

                self.console.insert(tk.END, f"- {setting}: {random.choice(values)}\n")

            elif setting in ghost_settings:

                values = ghost_settings[setting]['values']

                random.shuffle(values)

                self.console.insert(tk.END, f"- {setting}: {random.choice(values)}\n")

            elif setting in contract_settings:

                values = contract_settings[setting]['values']

                random.shuffle(values)

                selected_value = random.choice(values)

                if setting == "Cursed Possessions" and selected_value > 0:

                    items = contract_settings[setting]['items']

                    random.shuffle(items)

                    selected_items = ', '.join(items[:selected_value])

                    self.console.insert(tk.END, f"- {setting}: {selected_value} \n({selected_items})\n")

                else:

                    self.console.insert(tk.END, f"- {setting}: {selected_value}\n")



       

        # Remove dropdown and update options

        self.dropdown_value.set("1")

        self.dropdown_options = [str(i) for i in range(1, 26)]





    def toggle_theme(self):

       if self.theme == "light":

           self.theme = "dark"

           self.master.config(bg="black")

           self.console.config(bg="black", fg="white")

           self.button1.config(bg="black", fg="white")

           self.button2.config(bg="black", fg="white")

           self.button3.config(bg="black", fg="white")

           self.button4.config(bg="black", fg="white")

           self.dropdown.config()
           
           self.button5.config(bg="black", fg="white")

       else:

           self.theme = "light"

           self.master.config(bg="SystemButtonFace")

           self.console.config(bg="white", fg="black")

           self.button1.config(bg="SystemButtonFace", fg="black")

           self.button2.config(bg="SystemButtonFace", fg="black")

           self.button3.config(bg="SystemButtonFace", fg="black")

           self.button4.config(bg="SystemButtonFace", fg="black")

           self.dropdown.config(bg="SystemButtonFace", fg="black")
           
           self.button5.config(bg="SystemButtonFace", fg="black")





    def clear_console(self):

        self.console.delete(1.0, tk.END)





if __name__ == "__main__":

    root = tk.Tk()

    gui = GUI(root)

    root.mainloop()
