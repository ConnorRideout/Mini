from tkinter import Tk, Canvas, Button
from matplotlib.colors import Colormap
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from io import BytesIO
from pathlib import Path


vals = {
    "Anger": {
        "Critical": [
            "Disapproving",
            "Judgemental",
            "Sceptical"
        ],
        "Frustrated": [
            "Aggravated",
            "Agitated"
        ],
        "Rage": [
            "Furious",
            "Infuriated"
        ],
        "Bitter": [
            "Violated",
            "Indignant"
        ],
        "Envious": [
            "Resentful",
            "Jealous"
        ],
        "Hostile": [
            "Aggressive",
            "Provoked"
        ],
        "Humiliated": [
            "Ridiculed",
            "Disrespected"
        ],
        "Hatred": [
            "Betrayed",
            "Loathing"
        ],
        "Annoyed": [
            "Irritated",
            "Exasperated"
        ]
    },
    "Happy": {
        "Excited": [
            "Eager",
            "Energetic",
            "Enthusiastic"
        ],
        "Content": [
            "Pleased",
            "Satisfied",
            "Free"
        ],
        "Playful": [
            "Cheeky",
            "Amused"
        ],
        "Proud": [
            "Triumphant",
            "Successful",
            "Confident"
        ],
        "Optimistic": [
            "Hopeful",
            "Inspired",
            "Eager"
        ],
        "Accepted": [
            "Respected",
            "Valued"
        ],
        "Powerful": [
            "Courageous",
            "Creative"
        ],
        "Cheerful": [
            "Jovial",
            "Blissful",
            "Delighted"
        ],
        "Elated": [
            "Jubilant",
            "Euphoric"
        ],
        "Enthralled": [
            "Enraptured",
            "Enchanted"
        ],
        "Interested": [
            "Curious",
            "Inquisitive"
        ]
    },
    "Surprise": {
        "Startled": [
            "Stunned",
            "Shocked"
        ],
        "Confused": [
            "Disillusioned",
            "Perplexed"
        ],
        "Amazed": [
            "Astonished",
            "Awe-struck"
        ],
        "Overcome": [
            "Speechless",
            "Astounded"
        ],
        "Moved": [
            "Stimulated",
            "Touched"
        ]
    },
    "Bad": {
        "Bored": [
            "Indifferent",
            "Apathetic"
        ],
        "Busy": [
            "Pressured",
            "Rushed"
        ],
        "Stressed": [
            "Overwhelmed",
            "Out of control"
        ],
        "Tired": [
            "Sleepy",
            "Unfocussed"
        ],
        "Distant": [
            "Numb",
            "Withdrawn"
        ]
    },
    "Disgust": {
        "Repelled": [
            "Hesitant",
            "Reluctant"
        ],
        "Awful": [
            "Detestable",
            "Nauseated"
        ],
        "Affronted": [
            "Revolted",
            "Appalled"
        ],
        "Contempt": [
            "Dismissive",
            "Repugnance"
        ]
    },
    "Sad": {
        "Neglected": [
            "Isolated",
            "Lonely",
            "Abandoned"
        ],
        "Lost": [
            "Victimised",
            "Fragile"
        ],
        "Despair": [
            "Empty",
            "Depressed",
            "Sorrowful",
            "Grief",
            "Powerless"
        ],
        "Ashamed": [
            "Regretful",
            "Remorseful",
            "Guilty",
            "Embarrassed"
        ],
        "Suffering": [
            "Agony",
            "Hurt"
        ],
        "Disappointed": [
            "Dismayed",
            "Displeased"
        ],
        "Rejected": [
            "Persecuted",
            "Excluded"
        ]
    },
    "Fear": {
        "Nervous": [
            "Anxious",
            "Worried",
            "Dread"
        ],
        "Terrified": [
            "Hysterical",
            "Panicky"
        ],
        "Insecure": [
            "Inadequate",
            "Inferior",
            "Weak",
            "Insignificant",
            "Worthless"
        ],
        "Scared": [
            "Helpless",
            "Frightened"
        ],
        "Horrified": [
            "Mortified",
            "Aghast"
        ],
        "Threatened": [
            "Exposed",
            "Vulnerable"
        ]
    },
    "Love": {
        "Affectionate": [
            "Fondness",
            "Romantic"
        ],
        "Longing": [
            "Attraction",
            "Sentimental"
        ],
        "Desire": [
            "Infatuated",
            "Passionate",
            "Aroused"
        ],
        "Tenderness": [
            "Compassion",
            "Care"
        ],
        "Peaceful": [
            "Satisfied",
            "Relieved",
            "Thankful"
        ],
        "Trusting": [
            "Sensitive",
            "Intimate"
        ]
    }
}

inrsize = []
inrlbls = []
midsize = []
midlbls = []
outsize = []
outlbls = []
for key, val in vals.items():
    size = 0
    inrlbls.append(key)
    for mid, out in val.items():
        midsize.append(len(out))
        midlbls.append(mid)
        size += len(out)
        for o in out:
            outsize.append(1)
            outlbls.append(o)
    inrsize.append(size)


def on_exit():
    root.quit()
    root.destroy()


root = Tk()
root.protocol("WM_DELETE_WINDOW", on_exit)
root.geometry('1440x1440+100+0')


def getColorMap(steps: list[int], offset: bool = True) -> Colormap:
    ct = -(lout/20) if offset else 0
    o = []
    for step in steps:
        c = ct if ct >= 0 else (lout + ct)
        o.append(round(c))
        ct += step
    return cmap(o)


lout = len(outsize)
cmap = plt.get_cmap("hsv", lout)
inrclr = getColorMap(inrsize, False)
midclr = getColorMap(midsize)
outclr = getColorMap(outsize)

fig, ax = plt.subplots()

fig.patch.set_alpha(0)

kwargs = dict(rotatelabels=True,
              startangle=90,
              textprops={'family': 'Ebrima', 'size': 7,
                         'ha': 'center', 'va': 'center'},
              counterclock=False)

ax.pie(outsize,
       labels=outlbls,
       labeldistance=0.83,
       radius=1.5,
       colors=outclr,
       wedgeprops=dict(width=0.66, edgecolor='black', linewidth=0.5),
       **kwargs)

ax.pie(midsize,
       labels=midlbls,
       labeldistance=0.75,
       radius=1,
       colors=midclr,
       wedgeprops=dict(width=0.5, edgecolor='black', linewidth=0.5),
       **kwargs)

ax.pie(inrsize,
       labels=inrlbls,
       labeldistance=0.55,
       radius=0.5,
       colors=inrclr,
       wedgeprops=dict(edgecolor='black', linewidth=0.5),
       **kwargs)

ax.set(aspect='equal')

bimg = BytesIO()
plt.savefig(bimg, dpi=300)
img = Image.open(bimg).resize(size=(1440, 1440), box=(315, 55, 1655, 1395))


cnv = Canvas(root)
cnv.place(relwidth=1,
          relheight=1)

photo = ImageTk.PhotoImage(img)
cnv.create_image(0, 0, anchor='nw', image=photo)


def save():
    pth = Path(__file__).parent.joinpath('Emotion Wheel.png')
    pth.touch()
    img.save(pth)


btn = Button(root,
             text='Save',
             command=save)
btn.place(anchor='nw',
          x=5,
          y=5)

root.mainloop()
