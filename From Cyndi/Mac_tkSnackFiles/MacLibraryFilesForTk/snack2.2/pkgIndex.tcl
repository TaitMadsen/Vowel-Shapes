
# @@ Meta Begin
# Package snack 2.2
# Meta activestatetags ActiveTcl Public
# Meta as::author      {Kare Sjolander}
# Meta as::build::date 2013-11-13
# Meta as::origin      http://www.speech.kth.se/snack/
# Meta category        Audio recording, processing, and playing
# Meta description     The Snack sound extension adds commands to play and
# Meta description     record audio. Snack supports in-memory sound
# Meta description     objects, file based audio, and streaming audio, with
# Meta description     background audio processing. It handles fileformats
# Meta description     such as AIFF, AU, MP3, NIST/Sphere, and WAV. Snack
# Meta description     is {extensible;} new commands and sound file formats
# Meta description     can be added using the Snack C-library. Snack also
# Meta description     does sound visualization, e.g. waveforms and
# Meta description     spectrograms. The visualization canvas item types
# Meta description     update in real time and can output postscript.
# Meta license         BSD
# Meta platform        macosx-universal
# Meta require         {Tcl 8.4}
# Meta require         {Tk 8.4}
# Meta subject         sound audio wav aiff au mp3 visualization
# Meta summary         Recording, processing, and playing of audio
# @@ Meta End


if {![package vsatisfies [package provide Tcl] 8.4]} return

package ifneeded snack 2.2 [string map [list @ $dir] {
        # ACTIVESTATE TEAPOT-PKG BEGIN REQUIREMENTS

        package require Tcl 8.4
        package require Tk 8.4

        # ACTIVESTATE TEAPOT-PKG END REQUIREMENTS

          set dir {@}
        load [file join $dir libsnack.dylib];source [file join $dir snack.tcl]

        # ACTIVESTATE TEAPOT-PKG BEGIN DECLARE

        package provide snack 2.2

        # ACTIVESTATE TEAPOT-PKG END DECLARE
    }]
