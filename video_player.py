"""A video player class."""

from .video_library import VideoLibrary
from .video import Video
import textwrap
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self, playing = None, paused = None, playlists = None):
        self._video_library = VideoLibrary()
        self.playing = playing
        self.paused = paused
        if playlists is None:
            self.playlists = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        all_videos = sorted(self._video_library.get_all_videos(), key=lambda x: x.title)
        print("Here's a list of all available videos:")
        for video in all_videos:
            title = video._title
            video_id = video._video_id
            tags = video._tags
            num_tags = len(tags)
            print_tags = ""
            if num_tags != 0:
                for tag in range(0,1):
                    print_tags = print_tags + tags[tag]
            if num_tags > 1:
                for tag in range(1,num_tags):
                    print_tags = print_tags + " " + tags[tag]
            print(f"{title} ({video_id}) [{print_tags}]")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        all_video_ids = [item._video_id for item in self._video_library.get_all_videos()]
        if video_id not in all_video_ids:
            print("Cannot play video: Video does not exist")
        else:
            if self.playing == None and self.paused == None:
                playing = self._video_library.get_video(video_id)
                self.playing = playing
                print(f"Playing video: {playing._title}")
            else:
                if self.paused == None:
                    print(f"Stopping video: {self.playing._title}")
                    playing = self._video_library.get_video(video_id)
                    self.playing = playing
                    self.paused = None
                    print(f"Playing video: {playing._title}")
                else:
                    print(f"Stopping video: {self.paused._title}")
                    playing = self._video_library.get_video(video_id)
                    self.playing = playing
                    self.paused = None
                    print(f"Playing video: {playing._title}")

    def stop_video(self):
        """Stops the current video."""
        if self.playing == None:
            print("Cannot stop video: No video is currently playing")
        else:
            print(f"Stopping video: {self.playing._title}")
            self.playing = None

    def play_random_video(self):
        """Plays a random video from the video library."""
        choices = [item._video_id for item in self._video_library.get_all_videos()]
        self.play_video(random.choice(choices))

    def pause_video(self):
        """Pauses the current video."""
        if self.playing == None and self.paused == None:
            print("Cannot pause video: No video is currently playing")
        else:
            if self.paused != None:
                print(f"Video already paused: {self.paused._title}")
            else:
                self.paused = self.playing
                self.playing = None
                print(f"Pausing video: {self.paused._title}")

    def continue_video(self):
        """Resumes playing the current video."""
        if self.playing == None and self.paused == None:
            print("Cannot continue video: No video is currently playing")
        else:
            if self.paused == None:
                print("Cannot continue video: Video is not paused")
            else:
                self.playing = self.paused
                self.paused = None
                print(f"Continuing video: {self.playing._title}")

    def show_playing(self):
        """Displays video currently playing."""
        if self.playing == None and self.paused == None:
            print("No video is currently playing")
        else:
            if self.paused == None:
                title = self.playing._title
                video_id = self.playing._video_id
                tags = self.playing._tags
                num_tags = len(tags)
                print_tags = ""
                if num_tags != 0:
                    for tag in range(0,1):
                        print_tags = print_tags + tags[tag]
                if num_tags > 1:
                    for tag in range(1,num_tags):
                        print_tags = print_tags + " " + tags[tag]
                print(f"Currently playing: {title} ({video_id}) [{print_tags}]")
            else:
                title = self.paused._title
                video_id = self.paused._video_id
                tags = self.paused._tags
                num_tags = len(tags)
                print_tags = ""
                if num_tags != 0:
                    for tag in range(0,1):
                        print_tags = print_tags + tags[tag]
                if num_tags > 1:
                    for tag in range(1,num_tags):
                        print_tags = print_tags + " " + tags[tag]
                print(f"Currently playing: {title} ({video_id}) [{print_tags}] - PAUSED")
            

    def find_stored_playlist_name(self, playlist_name):
        stored_playlist_name = playlist_name
        for playlist in self.playlists:
            if playlist_name.upper() == playlist.upper():
                stored_playlist_name = playlist
        return stored_playlist_name

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        stored_playlist_name = self.find_stored_playlist_name(playlist_name)
        if stored_playlist_name in self.playlists:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self.playlists[playlist_name] = []
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        stored_playlist_name = self.find_stored_playlist_name(playlist_name)
        if stored_playlist_name not in self.playlists:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")

        elif stored_playlist_name in self.playlists and video_id not in [item._video_id for item in self._video_library.get_all_videos()]:
            print(f"Cannot add video to {playlist_name}: Video does not exist")

        else:
            if video_id in self.playlists[stored_playlist_name]:
                print(f"Cannot add video to {playlist_name}: Video already added")
            else:
                video_to_add = self._video_library.get_video(video_id)._title
                original_list = self.playlists[stored_playlist_name]
                original_list.append(video_id)
                self.playlists[stored_playlist_name] = original_list
                print(f"Added video to {playlist_name}: {video_to_add}")
        
    def show_all_playlists(self):
        """Display all playlists."""

        if len(self.playlists) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            for playlist in sorted(self.playlists):
                print(f"{playlist}")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        stored_playlist_name = self.find_stored_playlist_name(playlist_name)
        if stored_playlist_name not in self.playlists:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")

        else:
            print(f"Showing playlist: {playlist_name}")
            if len(self.playlists[stored_playlist_name]) == 0:
                print("No videos here yet")
            else:
                for video_id in self.playlists[stored_playlist_name]:
                    vid = self._video_library.get_video(video_id)
                    title = vid._title
                    video_id = vid._video_id
                    tags = vid._tags
                    num_tags = len(tags)
                    print_tags = ""
                    if num_tags != 0:
                        for tag in range(0,1):
                            print_tags = print_tags + tags[tag]
                    if num_tags > 1:
                        for tag in range(1,num_tags):
                            print_tags = print_tags + " " + tags[tag]
                    print(f"{title} ({video_id}) [{print_tags}]")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        stored_playlist_name = self.find_stored_playlist_name(playlist_name)

        if stored_playlist_name not in self.playlists:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        else:
            if video_id not in [item._video_id for item in self._video_library.get_all_videos()]:
                print(f"Cannot remove video from {playlist_name}: Video does not exist")
            elif video_id in [item._video_id for item in self._video_library.get_all_videos()] and video_id not in self.playlists[stored_playlist_name]:
                print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            else:
                video_to_remove = self._video_library.get_video(video_id)._title
                videos = self.playlists[stored_playlist_name]
                self.playlists[stored_playlist_name] = videos.remove(video_id)
                print(f"Removed video from {playlist_name}: {video_to_remove}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        stored_playlist_name = self.find_stored_playlist_name(playlist_name)
                    
        if stored_playlist_name not in self.playlists:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            self.playlists[stored_playlist_name] = []
            print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        stored_playlist_name = self.find_stored_playlist_name(playlist_name)

        if stored_playlist_name not in self.playlists:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:
            self.playlists.pop(stored_playlist_name)
            print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        print(f"Here are the results for {search_term}:")
        all_videos = sorted(self._video_library.get_all_videos(), key=lambda x: x.title)
        count = 0
        user_input_value = {}
        for x in range(0,len(all_videos)):
            if search_term.upper() in all_videos[x]._title.upper():
                title = all_videos[x]._title
                video_id = all_videos[x]._video_id
                user_input_value[x] = video_id
                tags = all_videos[x]._tags
                num_tags = len(tags)
                print_tags = ""
                if num_tags != 0:
                    for tag in range(0,1):
                        print_tags = print_tags + tags[tag]
                if num_tags > 1:
                    for tag in range(1,num_tags):
                        print_tags = print_tags + " " + tags[tag]
                count = count + 1
                print(f"{x+1}) {title} ({video_id}) [{print_tags}]")
        if count == 0:
            print(f"No search results for {search_term}")
        else:
            try:
                value = int(input("Would you like to play any of the above? If yes, specify the number of the video." +"\n" + "If your answer is not a valid number, we will assume it's a no.\n"))
                if value in range(1,count+1):
                    self.play_video(user_input_value[value-1])
                else:
                    print("Nope!")
            except ValueError:
                print("Nope!")
        
    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        print("search_videos_tag needs implementation")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
