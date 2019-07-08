# Taking Back August, Part I
# A tutorial visual novel by Robert Ciesla

# Our little inventory-system in pure Python
# the init-setting makes sure to run python-code before any other parts of the game

init python:
    items = []
    def display_items_overlay():
        if len(items)>0:
            inventory = "Briefcase: "
            for i in range(0, len(items)):
                item_name = items[i].title()
                if i > 0:
                     inventory += ", "
                inventory += item_name
            ui.frame()
            ui.text(inventory)
    config.overlay_functions.append(display_items_overlay)


# First we define the cast of characters and color-code them, like so:

define reg = Character("Reginald Pennelegion", color="#0099BB")
define merv = Character("Mervyn Popplewell", color="#007799")
define roy = Character("Royston Honeybun", color="#0044CC")
define rai = Character("Raine", color="#8888EE")
define cla = Character("Claire", color="#AA1100")
define man = Character("Overalls Man", color="#EE1100")

image rai serious = "rai_serious.png"

# Define sprites

image phone = "phone.png"

# Define backgrounds for office

image office = "office1.jpg"
image office2 = "office2.jpg"
image email = "email.jpg"
image topfloor = "topfloor.jpg"
image cooler = "cooler.jpg"

# Define backgrounds for the outdoor venues

image london = "london.jpg"
image london2 = "london2.jpg"
image park = "park1.jpg"
image park2 = "park2.jpg"

image alley = "alley.jpg"
image door = "door.jpg"
image window = "window.jpg"

image station = "station.jpg"

# Define images for the inferno-sequence;
# In each of its four locations the background will be randomized from this pool
# using the function "show_fire" (see further below)

image fire1 = "fire1.jpg"
image fire2 = "fire2.jpg"
image fire3 = "fire3.jpg"
image fire4 = "fire4.jpg"

# Define transitions

define slideleft = CropMove(2.0, "slideleft")
define fireflash = Fade(0.1, 0.0, 0.5, color="#e40")

# Define functions

label show_fire:
    $ num = renpy.random.randint(1, 4)
    $ which = "fire" + str(num)
    show expression which
    with fireflash
    return

label check_dvd:
    # play sound if "dvd_found" hasn't been set to "True" yet
    if dvd_found == False:
      play sound "sounds/sound.wav"
    $ if dvd_found == False: items.append("Pink DVD")
    $ if dvd_found == False: items.sort()
    $ if dvd_found == False: dvd_found = True
    return

label checktime:
    # call another function, show_fire, from within this function
    call show_fire

    play sound "sounds/woosh.wav"
    $ time -= 5
    if time < 5:
      jump burn
    return


# The game starts here.

label start:

# Define variables

    $ sips = 0
    $ time = 0
    $ items = []
    $ dvd_found = False

    # Play a sound effect after 1.5 seconds of silence
    play sound [ "<silence 1.5>", "sounds/mouse_clicks.wav" ]

    show office1
    with slideleft

    # Room 1: Reginald's Desk

    show reg:
        xalign 0.0
        xpos 0.7
        ypos 0.2
    with easeinleft

    "You, Reginald Pennelegion, a government cyber security expert and our protagonist, are browsing nonsense at your desk workstation."

    "You're supposed to be working on a big project, but instead you're drifting into a world of memes, online auctions, and silly video clips."

    "You are still depressed about the passing of your best and only friend at the office, one Mervyn Popplewell.."

    # Your Desk
    menu deskaction:
     "Choose your action"

     "Visit the drinking station":
         $ time += 1
         stop sound fadeout 1.0
         hide office1
         show cooler
         with dissolve
         jump drinkingfountain

     "Examine your colleague's desk":
         $ time += 1
         stop sound fadeout 1.0
         hide office1
         show office2
         with dissolve
         jump neighboringdesk

    menu drinkingfountain:

             "Choose your action"

             "Return to your desk":
                 show office1
                 with dissolve
                 jump deskaction

             "Drink":
                 $ sips += 1
                 play sound "sounds/gulp.wav"

                 if sips<3:
                     "Gulp. You take sip number [sips]."
                     show office1
                     with dissolve
                     jump deskaction
                 elif sips==3:
                     "Gulp. You are beginning to feel full at sip number [sips].."
                     show office1
                     with dissolve
                     jump deskaction
                 else:
                     "You decided it was best to stop drinking."
                     show office1
                     with dissolve
                     jump deskaction

    label neighboringdesk:

           if time>3:
               jump emailreceived

           if time<=2:
               "One of your colleagues left early. His desk is much tidier than yours."
               hide office2
               show office1
               with dissolve
               show reg
               jump deskaction
           else:
               "Yes, the desk next to yours is rather tidy."
               hide office2
               show office1
               with dissolve
               show reg
               jump deskaction

    # Email time
    label emailreceived:
        scene email
        with dissolve

        play sound "sounds/email.wav"

        "No time for that now! Your workstation sounds off. You've received email."
        "You open the message. It says: 'Meet me at Hyde Park at seven pm tonight. I'll be by the Wellington Arch. Don't tell anyone..'"
        "'..signed Mervyn Popplewell'"
        "This is some kind of sick joke. Mervyn is gone."
        "You decide to investigate the origin of the email by phoning Royston at tech support.."
        "After a phone call upstairs, it becomes apparent the email is genuine. Royston asks you to fetch something from the top floor."

label topfloor:

    scene topfloor
    with dissolve

    # Show the phone-sprite at specific coordinates
    show phone:
        xalign 0.0
        xpos 0.5
        ypos 0.18
    with easeinleft

    "You locate a mobile phone in an obscure location. It's really quite old, looking like it dates back to the 80s. You pick it up."

    hide phone
    with easeoutright

    play sound "sounds/sound.wav"
    $ items.append("special phone")

    scene london
    with dissolve

   # If they player took their time drinking water, display a message
    if sips >= 3: 
        "You feel the need to use the bathroom, but you are in a hurry.."
    "You decide to follow the instructions in the strange email. Hyde Park, here we come."

   # Hyde Park
    label hydepark:
    play music [ "sounds/park.mp3" ] fadein 10.0 loop

    scene park
    with dissolve

    "Hyde Park is just a walking distance from the office. It's getting darker as you make your way past busy Londoners. The Wellington Arch now looms in the distance. "
    $ items.append("coin")  

    # Sort the items-list
    $ items.sort()

    play sound "sounds/sound.wav"
    "You notice a coin in the ground. You pick it up and pocket it."

    scene park2
    with dissolve

    "You arrive at the Wellington Arch, on time. No-one is there to greet you."
    "You wait for quite a while, but not a soul approaches you."
    "Disappointed, you begin the trip home."

    # Office Inferno
    label inferno:

    "Your disappointment doesn't last long. You see flames in the distance!"
    reg "Maybe if I'd done some overtime instead of going to Hyde Park I could've prevented this!"
    play sound "sounds/phone.wav" loop

    "Panicking, Reginald is alarmed by the phone in his briefcase. The ancient thing is ringing. You answer the call."

    stop sound
    show roy:
        xalign 0.0
        xpos 0.2
        ypos 0.2
    with easeinright

    roy "Get the pink DVD and get it out of there. You have ten minutes before its devoured by fire."

    hide roy
    play sound "sounds/siren.wav" fadein 5.0 fadeout 5.0

    "It's about August, the prototype for the first fully cyber-attack proof firewall to be implemented in all of Her Majesty's agencies later this year. "
    
    # The Inferno Proper
    label actionscene:

    scene alley
    with dissolve

    play music [ "sounds/fireplace.mp3" ] fadein 10.0 loop

    "You reach the back alley of the office building, feeling a sense of urgency. It's now or never. You climb up the fire ladder."
    $ time = 25

    call show_fire

    # Set-up and display particles using the SnowBlossom-effect
    image sparks = Fixed(
        SnowBlossom(im.FactorScale("images/fireparticle.png",1.0),count=12,start=5),
        SnowBlossom(im.FactorScale(im.Alpha("images/fireparticle.png",0.8),0.6),count=15,yspeed=(50,125)))

    show sparks

    menu officefire:
     "Choose your action. You have [time] seconds left. You are in the general office area."
     "Dash to your desk":
         call checktime
         jump firedesk_a

     "Dash to your colleague's desk":
         call checktime
         jump firedesk_b

     "Dash to your other colleague's desk":
         call checktime
         call check_dvd
         jump firedesk_c

    menu outwindow:
     "Choose your action. You have [time] seconds left. You are in the general office area."
     "Climb Out the Window":
         call checktime
         jump window

     "Dash to your desk":
         call checktime
         jump firedesk_a

     "Dash to your colleague's desk":
         call checktime
         jump firedesk_b

     "Dash to your other colleague's desk":
         call checktime
         call check_dvd
         jump firedesk_c

    menu firedesk_a:
     "Choose your action. You have [time] seconds left. You are at your own desk. You find nothing but flames here."

     "Dash to the general office area":
         call checktime
         if dvd_found == False:
              jump officefire
         else:
              jump outwindow

     "Dash to your colleague's desk":
         call checktime
         jump firedesk_b

     "Dash to your other colleague's desk":
         call checktime
         call check_dvd
         jump firedesk_c

    menu firedesk_b:
     "Choose your action. You have [time] seconds left. You are at your colleague's desk. You find nothing but smoke here."

     "Dash to the general office area":
         call checktime
         if dvd_found == False:
              jump officefire
         else:
              jump outwindow

     "Dash to your desk":
         call checktime
         jump firedesk_a

     "Dash to your other colleague's desk":
         call checktime
         call check_dvd
         jump firedesk_c

    menu firedesk_c:
     "Choose your action. You have [time] seconds left. You are at your other colleague's desk."

     "Dash to the general office area":
         call checktime
         if dvd_found == False:
              jump officefire
         else:
              jump outwindow

     "Dash to your desk":
         call checktime
         jump firedesk_a

     "Dash to your colleague's desk":
         call checktime
         jump firedesk_b

label burn:
    "You pass out from the fumes and burn to death."
    if dvd_found == True:
        "They find your corpse clutching a scorched pink DVD.."

    # Back to main menu
    $ renpy.full_restart()

label window:

    scene alley
    with dissolve

    stop music fadeout 5.0

    "You find your way out of the window and slide down the hot fire ladder!"

    $ randomdialogue = renpy.random.choice(['The phone in the briefcase rings again.', 'You are startled by a shrill noise emanating from your briefcase.', 'The ancient mobile phone is ringing.'])

    play sound "sounds/phone.wav" loop

    # Display our random dialogue
    "[randomdialogue]"

    stop sound
    show roy:
        xalign 0.0
        xpos 0.2
        ypos 0.2
    with dissolve

    roy "Well done. Go home and stay there for further instructions. Protect the disc with your life, if necessary."
   
    # Generate a random number between 20 and 80
    $ random_number = renpy.random.randint(20, 80)

    "You feel [random_number]%% motivated to continue your quest!"

label home:

    scene london2
    with dissolve

    # We use the music-channel to play ambient sounds. This is because only this channel
    # allows for both the looping and the fadein for audio
    play music [ "sounds/london_bridge.wav" ] fadein 10.0 loop

    "The adrenaline begins to slowly wear off as you pace towards your residence." 

    play sound "sounds/phone.wav" loop

    "The old phone rings again."
    stop sound

    "This time, it's a woman's voice."
   
    # Show the serious face for Raine
    show rai serious:
        xalign 0.0
        xpos 0.2
        ypos 0.2
    with dissolve

    rai "{i}Whatever you do, don't go home!{/i} Leave London right {u}now.{/u} Go as far North as you can. A train is your best bet."
    rai "I'll call again. Go! {b}And don't lose the disc!{/b}"

    # Hide serious Raine and show her more cheeky face
    hide rai
    show rai:
        xalign 0.0
        xpos 0.2
        ypos 0.2

    rai "Oh, and, why not visit {a=http://www.robertciesla.com}this great site{/a} when you have the time?"
    rai "I personally visit that {size=+10}{i}fascinating{/i}{/size} website every day."
    hide rai

    # Replace the ambient sound with another one 
    play music [ "sounds/ambience.wav" ] fadein 10.0 loop

    # Again, the music-channel is great for ambience, too, for its versatility with options

    $ renpy.movie_cutscene("videos/Interlude.webm")
    scene door
    with dissolve

    "You hear a strange humming noise coming from your flat. Putting your ear against the door, {cps=5}the noise gets louder.{/cps}"

    "{k=-1.5}Something is up.{/k} {k=1.5}You decide to heed the girl's advice and leave.{/k}"
    scene window
    with dissolve

    "Running down the street toward the train station you look back once more.{vspace=25}{w}A human-like figure with unnaturally large eyes stares back."

    "It's dressed in light blue uniform, briefly reminding you of a life-sized action figure of some kind.{fast} Your heart skips a beat or two."

    scene station
    with dissolve
    stop music fadeout 5.0

    "After running what felt like a marathon, you reach Euston train station, panting heavily. No one seems to have been following you."
    "You remember the girl's advice and look for the next northbound train.."
    "You've now reached the end of this tutorial visual novel. Check out the source code to learn more."