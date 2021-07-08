![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png)
### General Assembly, Software Engineering Immersive 

# note-it-down 
By [Guy Kozlovskij](https://github.com/guykozlovskij) and [Chris Wood](https://github.com/Chrisw00d1).

A Django, PostgreSQL, React full-stack app. This is the final project for General Assembly's Software Engineering Immersive course.

**note-it-down** is a fun and simple music maker allowing users to create and share songs.

## [Try it out!](https://note-it-down-app.netlify.app/)

![](/readme-img/intro.gif)

Project frontend can be found [here](https://github.com/guykozlovskij/project-4-client).

## Table of Contents
* [Overview](#overview)
* [Brief](#brief)
* [Technologies Used](#technologies)
* [Approach](#approach)
  * [Whiteboarding](#whiteboarding)
    * [Models](#models)
    * [Splitting the Workload](#workload)
* [Backend](#backend)
  * [Models and Database](#models-and-db)
  * [Views](#views)
* [Frontend](#frontend)
  * [Tone.js](#tone)
  * [Splitting Up](#splitting)
    * [The Design](#design)
    * [Song Index](#index)
    * [Song Expanded](#expanded)
    * [Playing the Songs](#playing)
    * [The Grid](#grid)
    * [Navbar](#navbar)
* [Final Thoughts](#thoughts)
  * [Wins and Challenges](#wins)
  * [Lessons Learned](#lessons)
  * [Improvements](#improvements)

<a name="overview"></a>

## Overview
For our fourth and final project at **General Assembly's Software Engineering Immersive Course** we were given 7 days to build a full stack website. After some consideration we deiced to build something that allows users to create and share their creations. 

**note-it-down** was born - an app to make short tunes in the scale of C major. 

We deployed our app using [Heroku](https://www.heroku.com/) and [Netlify](https://www.netlify.com/).

<a name="brief"></a>

## Brief
- Choose to work as either a pair, group or solo
- Build a full-stack application by making our own backend and frontend 
- Use a Python Django API, using Django REST Framework to serve our data from a PostgresSQL database
- Consume the API with  a separate frontend built with React
- Build a complete product, which most likely means multiple relationships and CRUD functionality for at least a couple of models
- Have a visually impressive design 
- Have it deployed online so it's publicly accessible

<a name="technologies"></a>

## Technologies Used
- JavaScript (ES6)
- Python
- Django
- PostgreSQL
- React.js
- Tone.js
- SCSS
- HTML5
- Git and GitHub
- Cloudinary
- Google Chrome Dev Tools
- Noun Project
- Excalidraw
- Heroku and Netlify

<a name="approach"></a>

## Approach 
We started by planning-out the layout of our website and understanding exactly how we would like to style it. We knew our models would not be very complex, so our focus was to complete the backend in 2 days and transition into working with **Tone.js** and making our app look stunning.

<a name="planning"></a>

### Planning

<a name="whiteboarding"></a>

#### Whiteboarding
From the very beginning, we had a good sense of direction and an idea of what the project will look like. The vision was clear, and in the end the final product closely resembled the initial sketch we made on [Excalidraw](https://excalidraw.com/).

![](/readme-img/comparison.png)

<a name="models"></a>

#### Models
On the same day we also planned-out our models. We knew there would not be any complex relationship, as the focus of the user experience is the creation of songs. We decided to keep it simple and only have three models. 

![](/readme-img/erd.png)

<a name="workload"></a>

#### Splitting the Workload
Once everything has been planned-out we proceeded to split up, with Chris starting to work with **Tone.js** in the frontend while I went to build the backend. 

<a name="backend"></a>

## Backend
I started out by scaffolding the backend, adding the PostgreSQL database, installing dependencies and setting up the Django apps for the backed.

<a name="models-and-db"></a>

### Models and Database
I first started working on our models. Once the **user** model has been setup I moved on to the **song** model which contained one of our main challenges - storing the songs.

After spending some time with **Tone.js** in the frontend, Chris understood that we will be storing the `notes` for songs in arrays of boolean values, one for each of the grid blocks. 

<a name="no-notes"></a>

```js
export default function noNotes() {
  return {
    c5: [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
    b4: [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
    a4: [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
    g4: [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
    f4: [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
    e4: [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
    d4: [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
    c4: [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
  }
}
```

Knowing this, I went to read Django documentation to look for a way we can save our `notes` in the database. To my surprise, the solution was simple and elegant. Using `JSONField` we can send the `notes` as a valid JSON object and easily retrieve them from our API. 

![](/readme-img/api.png)

Additionally our **song** model also contained a `ManyToManyField` for storing likes and a `PositiveIntegerField` to store our tempo as a number.

```py
class Song(models.Model):
    name = models.CharField(max_length=20)
    notes = models.JSONField()
    liked_by = models.ManyToManyField(
        'jwt_auth.User',
        related_name='liked_songs',
        blank=True
    )
    tempo = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(180)]
    )
    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name='created_songs',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name}'
```

<a name="views"></a>

### Views
Upon finishing the serializers for the models and implementing authentication I moved on to creating the views and testing them in `client.http` as I went along. The process went by smoothly which is a testament to how far we have gone in the course. 

In addition to commenting and full **CRUD** functionality for songs we also wanted users to be able to like and unlike songs. I was happy to learn I could write this functionality in a single view. 

```py
class SongLikedView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        try:
            song_to_like = Song.objects.get(pk=pk)
            if request.user in song_to_like.liked_by.all():
                song_to_like.liked_by.remove(request.user.id)
            else:
                song_to_like.liked_by.add(request.user.id)
            song_to_like.save()
            serialized_song = PopulatedSongSerializer(song_to_like)
            return Response(serialized_song.data, status=status.HTTP_202_ACCEPTED)
        except Song.DoesNotExist:
            raise NotFound()
```

I discovered that unlike with Express, which I worked on in the previous project, many things in Django are very streamlined as simplified, such as cascading in deletion. 

<a name="frontend"></a>

## Frontend
Once the backend was put into place, I rejoined Chris to continue working on the frontend. **Tone.js** was used for our sound grid and we spent much time studying it and reading the documentation. 

<a name="tone"></a>

### Tone.js
By the time I joined Chris, he already had made major steps forward with **Tone.js**, and has set up most of the player. 

The grid of notes was set in the `noNotes` hook show [previously](#no-notes) and assigned in the `Grid` where our music player lives.

```js
import noNotes from '../hooks/noNotes.js'

const [allNotes, setAllNotes] = useState(savedSong ? savedSong.allNotes : noNotes)
```

We used `PolySynth` as the synthesizer of our choice.

```js
const gain = new Tone.Gain(0.1).toDestination()
const synths = new Tone.PolySynth().connect(gain)
const notes = Object.keys(allNotes)
```

The repeater then plays the notes in a sequence working in a similar way as a `setInterval`. We also used the repeater to highlight the currently playing notes in our `<IndividualButton>`, by setting a class and transforming in CSS. 

```js
const repeat = (time) => {
  const step = stepper % 16
  setWhichBox(step)
  notes.forEach((note) => {
    if (allNotes[note][step]) {
      synths.triggerAttackRelease(note, '8n', time)
    }
  })
  stepper++
}
```

<a name="splitting"></a>

### Splitting Up 
We once again decided to split the workload. As Chris went on to work on functionalities such register, login, cloning and editing songs, I proceeded build the Song Index page, Song Expanded view and took the lead establishing a visual theme for our website. 

<a name="design"></a>

#### The Design
Inspired by iOS, I wanted our website to have a beautiful minimalist look using a pastel palette and frosted glass effect to closely resemble an iPhone homepage.

<a name="index"></a>

#### Song Index 
I started building the song index page by making simple GET request for the songs and proceeded to create and elegant card to display them.

![](/readme-img/song-index.png)

Although the play button would transform if a song is played we realized it may still be easy for a user to loose track of the source of music. We implemented a beautiful highlight around our card to make it pop visually. 

![](/readme-img/play.gif)

Since we were driven by a minimalist theme we decided to only keep a name and a few buttons on our cards. This gave birth to the expanded view. 

<a name="expanded"></a>

#### Song Expanded 
The expanded view contains most of the functionality allowing owners to edit and delete and authenticated users to comment and clone. 

![](/readme-img/expanded.gif)

<a name="playing"></a>

#### Playing the Songs
Playing songs required implementing Tone.js once more and this time passing the notes from our API to the player, rather than taking them from the grid. 

```js
const playSong = async (e) => {
    await Tone.Transport.stop()
    await Tone.Transport.clear(transportEventId.current)
    let newPlay = false

    allNotes = { ...filteredSongs(songs, filter, sub, filterBy)[e.target.name].notes }
    const notes = Object.keys(allNotes)

    if (id === filteredSongs(songs, filter, sub, filterBy)[e.target.name].id) {
      setId(null)
    } else {
      newPlay = true
      setId(filteredSongs(songs, filter, sub, filterBy)[e.target.name].id)
      await Tone.Transport.stop()
      await Tone.Transport.clear(transportEventId.current)

    }
```

This only had to be done in the `SongIndex`. We managed to use the same `playSong` function in both the index and expanded view to have a seamless experience of playing and switching between songs and views by passing it from one component to another.

```js
{ expandingId && <Expanding 
  songs={filteredSongs(songs, filter, sub, filterBy)} 
  expandingId={expandingId} 
  playSong={playSong} 
  id={id} 
  setUpdate={setUpdate} 
  update={update} 
  handleExpand={handleExpand} 
  setExpandingId={setExpandingId} />}
```

<a name="grid"></a>

#### The Grid
In the designing of the Grid, we selected a pastel palette with beautiful colours making the process of placing notes warm and welcoming. Each of the rows is assigned the same colour helping the user identify the notes visually in addition to hearing the note on click. 

![](/readme-img/grid.gif)

<a name="navbar"></a>

#### Navbar
Finally, to preserve the clean look of the website, instead of having persistent navbar at the top, Chris implemented a beautiful sidebar which we designed using the frosted glass effect seen throughout the whole app. 

![](/readme-img/nav.gif)

<a name="thoughts"></a>

## Final Thoughts

<a name="wins"></a>

### Wins and Challenges
- **Tone.js**: working with this library was not easy and required thorough reading of documentation and studying other people's applications. Although we are happy with the final product we could not prevent the player braking when using the app for too long or placing too many notes.  

- **Responsive Design**: Due to us being on track with development and always moving along at a good pace, we had 1 day to try and make "note-it-down" mobile friendly. We are incredibly happy with how it turned out as it really gave the app the feeling of being a finished product. 

![](/readme-img/mobile.gif)

<a name="lessons"></a>

### Lessons Learned
- **Having Fun is Key**: This project has been hands down the most enjoyable to work on. I believe this is due to us making something we genuinely enjoyed playing with as well as keeping the scale of the project neither too big or too small. Although we did encounter roadblocks, we could take a break and any point and just go and make some music 🎹🎶.

<a name="improvements"></a>

### Improvements
- We would like to comeback to **Tone.js** having better understanding of it and fix the sound breaking issues.
- Optimizing for different sized phone screens by adding more responsiveness.
