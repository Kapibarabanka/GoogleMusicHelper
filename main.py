from gmusicapi import Mobileclient


def log_in(api: Mobileclient):
    print("You need to log in to continue:")
    api.perform_oauth()
    if not api.oauth_login(Mobileclient.FROM_MAC_ADDRESS):
        print("Something went wrong with authentication")
        return False
    print("Logged in successfully")
    return True


def run_menu(api: Mobileclient):
    print()
    print("""Choose what you want to do:
    1. Create backup
    2. Load from backup
    3. Migrate to another account
    4. Change account
    5. Exit""")
    choice = input()
    if choice == "1":
        create_backup()
    elif choice == "2":
        load_from_backup()
    elif choice == "3":
        migrate()
    elif choice == "4":
        api.logout()
        print("Logged out!")
        print()
        if not log_in(api):
            return
    elif choice == "5":
        print("Goodbye!")
        return
    else:
        print("Unknown command")
    run_menu(api)


def create_backup(add_songs=True, add_playlists=True):
    songs = sorted(api.get_all_songs(), key=lambda s: s["title"])
    if add_songs:
        backup_songs(songs)
    if add_playlists:
        backup_playlists(songs)


def backup_songs(songs: list):
    backup_file = open("all_songs.txt", "w", encoding='utf-8')
    info_file = open("all_songs_info.txt", "w", encoding='utf-8')
    uploaded_file = open("uploaded_songs_info.txt", "w", encoding='utf-8')
    for song in songs:
        try:
            backup_file.write(song["storeId"] + "\n")
            info_file.write("{0} - {1}\n".format(song["artist"], song["title"]))
        except KeyError:
            uploaded_file.write("{0} - {1}\n".format(song["artist"], song["title"]))
    backup_file.close()
    info_file.close()
    uploaded_file.close()


def backup_playlists(songs: list):
    playlists = api.get_all_user_playlist_contents()
    backup_file = open("all_playlists.txt", "w", encoding='utf-8')
    info_file = open("all_playlists_info.txt", "w", encoding='utf-8')
    for playlist in playlists:
        backup_file.write(playlist['name'] + '\n')
        info_file.write("{0} ({1})\n".format(playlist['name'], playlist['id']))
        for track in playlist['tracks']:
            backup_file.write(track['trackId'] + ' ')
            try:
                track_info = track['track']
            except KeyError:
                track_info = list(filter(lambda s: s['id'] == track['trackId'], songs))[0]
            info_file.write("\t{0} - {1}\n".format(track_info["artist"], track_info["title"]))
        backup_file.write("\n")
        info_file.write("\n")
    backup_file.close()
    info_file.close()


def load_from_backup():
    print("not implemented yet :c")


def migrate():
    print("not implemented yet :c")


def print_help():
    print("not implemented yet :c")


if __name__ == '__main__':
    print("Hello!")
    api = Mobileclient()
    isLoggedIn = api.oauth_login(Mobileclient.FROM_MAC_ADDRESS)
    if not isLoggedIn:
        isLoggedIn = log_in(api)
    if isLoggedIn:
        run_menu(api)
