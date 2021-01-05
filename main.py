__version__ = '2018.07.23'
__author__ = 'Alexis BOURGET'

import os
import re
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
# For errors when downloading
import urllib.error

import utilities.constants as cst
import utilities.tools as tls
import utilities.story_writer as sw
import utilities.data_handler as dh


class UI(tk.Frame):
    """
    The UI for the app. Contains the main function which launches the app.
    """
    @classmethod
    def main(cls):
        """Main function. Launches the app"""

        root = tk.Tk()
        root.title(cst.APP_NAME)
        root.minsize(cst.MIN_SIZE_X, cst.MIN_SIZE_Y)

        cls(root)
        root.mainloop()
        tls.setup_logging('main').info('Quitting application')

    def __init__(self, master: tk.Tk):

        super(UI, self).__init__(master)

        self.__master = master
        self.__base_folder = os.getcwd()

        try:
            main_folder = tls.get_settings()[0]
        except FileNotFoundError:
            main_folder = tls.popup_settings(self.__master)
            with open('settings.ffndl', 'w', encoding='utf-8') as f:
                f.write(main_folder + '\n')

        self.__main_folder = main_folder
        os.chdir(self.__main_folder)

        UI.__setup_folders()
        # Setup-ing logging
        self.__logger = tls.setup_logging('UI', True)
        with open(cst.LOGFILE_NAME, 'a', encoding='utf-8') as lf:
            lf.write('\n')
        tls.setup_logging('main').info('Starting up application')
        # Removes the older log files
        log_files = sorted(os.listdir('0/logs'))
        while len(log_files) > cst.MAX_LOG_FILE:
            title = log_files.pop(0)
            if re.fullmatch(r'\d{8}.log', title) is not None:
                os.remove(f'0/logs/{title}')
                self.__logger.info(f'Removed {title}')

        # Initialize the connection to the database
        self.__database = dh.DataHandler('0/data/ffndl_database.db')

        # Initialize the story writer
        self.__writer = sw.StoryWriter()

        # For the left pane
        self.__selectable_stories = []
        # For the right pane
        self.__selected_stories = []
        self.__selected_var = []

        self.__selected_site = tk.StringVar()
        self.__selected_sort = tk.StringVar()
        self.__url_entered = tk.StringVar()

        # The existing TopLevel windows
        self.__top_levels = []

        self.__logger.debug('Making menus')
        self.__make_menus()
        self.__logger.debug('Menus made')
        self.__logger.debug('Making frames')
        self.__make_frames()
        self.__logger.debug('Frames made')

        # Default choices for the site and the sort selector (by title)
        self.__logger.debug('First sorting and display')
        self.__site_selector.current(0)
        self.__sort_selector.current(6)
        # The default choices have been made, they are now accounted for
        self.__update_selectable_display()

    @staticmethod
    def __setup_folders():
        """
        Ensure all important folders are present
        """
        for path in cst.FOLDERS:
            if not os.path.isdir(path):
                os.makedirs(path)

    def __change_save_folder(self):
        """
        Allows the user to change their save folder
        """
        self.__logger.info('Changing save folder')
        for window in self.__top_levels:
            window.destroy()

        folder = tls.popup_settings(self)
        os.chdir(self.__base_folder)
        if folder != '':
            with open('settings.ffndl', 'w', encoding='utf-8') as f:
                f.write(folder + '\n')
            mb.showinfo(
                message=f'This change from {self.__main_folder} to {folder}'
                        f' will only take effect once you restart the app.'
            )
        os.chdir(self.__main_folder)
        self.__logger.debug('Save folder changed')

    def __make_menus(self):
        """
        Build the menu for the app
        """
        menu_bar = tk.Menu(self.__master)

        menu_stories = tk.Menu(menu_bar,
                               tearoff=0)
        menu_stories.add_command(
            label='Update stories',
            command=lambda: self.__handle_stories('update')
        )
        menu_stories.add_command(
            label='Download stories',
            command=lambda: self.__handle_stories('download')
        )
        menu_stories.add_separator()
        menu_stories.add_command(
            label='Download informations',
            command=lambda: self.__handle_stories('informations')
        )
        menu_stories.add_separator()
        menu_stories.add_command(label='Delete stories',
                                 command=lambda: self.__delete_stories())
        menu_bar.add_cascade(label='Stories',
                             menu=menu_stories)

        menu_stats = tk.Menu(menu_bar,
                             tearoff=0)
        menu_stats.add_command(
            label='For selected site',
            command=lambda: self.__do_statistics(self.__selected_site.get())
        )
        menu_stats.add_command(label='For each site',
                               command=lambda: self.__each_site_statistics())
#        NOT IMPLEMENTED YET
#        menu_stats.add_separator()
#        menu_stats.add_command(label='General statistics',
#                               command=self.__general_statistics)
        menu_bar.add_cascade(label='Statistics',
                             menu=menu_stats)

        menu_mark = tk.Menu(menu_bar,
                            tearoff=0)
        menu_mark.add_command(label='Read',
                              command=lambda: self.__read_or_unread('read'))
        menu_mark.add_command(label='Unread',
                              command=lambda: self.__read_or_unread('unread'))
        menu_bar.add_cascade(label='Mark as',
                             menu=menu_mark)

        menu_series = tk.Menu(menu_bar,
                              tearoff=0)
        menu_series.add_command(label='Add to',
                                command=lambda: self.__add_to_series())
        menu_series.add_separator()
        menu_series.add_command(label='Delete series',
                                command=lambda: self.__delete_series())
        menu_bar.add_cascade(label='Series',
                             menu=menu_series)

        menu_settings = tk.Menu(menu_bar,
                                tearoff=0)
        menu_settings.add_command(label='Change save folder',
                                  command=self.__change_save_folder)
        menu_bar.add_cascade(label='Settings',
                             menu=menu_settings)

        self.__master.config(menu=menu_bar)

    def __make_selectable_part(self, parent: tk.PanedWindow) -> tk.LabelFrame:
        """
        Makes the 'selectable' part of the UI (the one on the left)

        :param parent: the Paned Window which allows resizing inside of the main
                       frame
        :return the label frame containing the 'selectable' part
        """
        l_frame = tk.LabelFrame(parent, text='Stories present locally',
                                padx=2, pady=2)

        site_frame = tk.LabelFrame(l_frame, text='Site', padx=2, pady=0)

        self.__site_selector = ttk.Combobox(site_frame,
                                            textvariable=self.__selected_site,
                                            state='readonly')
        self.__site_selector['values'] = sorted(list(cst.SITES.keys()))
        self.__site_selector.bind('<<ComboboxSelected>>',
                                  lambda _: self.__select_site())

        sort_frame = tk.LabelFrame(l_frame, text='Sort by', padx=2, pady=2)

        self.__sort_selector = ttk.Combobox(sort_frame,
                                            textvariable=self.__selected_sort,
                                            state='readonly')
        self.__sort_selector['values'] = list(cst.SORT_OPTIONS.keys())
        self.__sort_selector.bind('<<ComboboxSelected>>',
                                  lambda _: self.__select_sort())

        self.__selectable_listbox = tk.Listbox(l_frame, selectmode='extended')
        self.__selectable_listbox.bind('<Double-1>',
                                       lambda _: self.__selectable_command())
        self.__selectable_listbox.bind('<Return>',
                                       lambda _: self.__selectable_command())

        self.__site_selector.pack(fill=tk.X)
        site_frame.pack(fill=tk.X)

        self.__sort_selector.pack(fill=tk.X)
        sort_frame.pack(fill=tk.X)

        self.__selectable_listbox.pack(fill=tk.BOTH, expand=tk.YES)

        l_frame.pack(fill=tk.BOTH, expand=tk.YES)

        return l_frame

    def __make_selected_part(self, parent: tk.PanedWindow) -> tk.LabelFrame:
        """
        Make the 'selected' part of the UI (the one on the right)

        :param parent: the Paned Window which allows resizing inside of the main
                       frame
        :return the label frame containing the 'selected' part
        """
        l_frame = tk.LabelFrame(parent, text='Selected stories',
                                padx=5, pady=5)

        url_box = tk.Entry(l_frame, textvariable=self.__url_entered)
        url_box.bind('<Return>', lambda _: self.__url_command())

        self.__selected_listbox = tk.Listbox(l_frame, selectmode='extended')
        self.__selected_listbox.bind('<Double-1>',
                                     lambda _: self.__selected_command())
        self.__selected_listbox.bind('<Return>',
                                     lambda _: self.__selected_command())
        self.__selected_listbox.bind('<Button-2>',
                                     lambda _: self.__copy_command())

        url_box.pack(fill=tk.X)
        self.__selected_listbox.pack(fill=tk.BOTH, expand=tk.YES)

        l_frame.pack(fill=tk.BOTH, expand=tk.YES)

        return l_frame

    def __make_frames(self):
        """
        Ensure the 'selectable' and 'selected' part are created and put inside
        the paned window
        """
        panned = tk.PanedWindow(self.__master, orient=tk.HORIZONTAL)

        self.__logger.debug('Making selectable part')
        panned.add(self.__make_selectable_part(panned))
        self.__logger.debug('Selectable part made')
        self.__logger.debug('Making selected part')
        panned.add(self.__make_selected_part(panned))
        self.__logger.debug('Selected part made')

        panned['sashwidth'] = 8

        panned.pack(side=tk.TOP, expand=tk.Y, fill=tk.BOTH, pady=2, padx=2)

    def __select_site(self):
        """
        Allow the user to select a site in which to select stories
        """
        self.__logger.info('Selecting a site')
        self.__site_selector.selection_clear()
        # Replace at the beginning
        self.__selectable_listbox.see(0)
        self.__logger.debug('Site selected')
        self.__update_selectable_display()

    def __select_sort(self):
        """
        Allow the user to arrange the story are displayed according to a
        specific sorting method
        """
        self.__logger.info('Selecting the sorting method')
        self.__sort_selector.selection_clear()
        self.__logger.debug('Sorting method selected')
        self.__update_selectable_display()

    def __selectable_command(self):
        """
        Allow the user to select stories from the one already present in the
        database
        """
        self.__logger.debug('Selecting URLs')
        # Update the concerned lists
        indexes = self.__selectable_listbox.curselection()

        # Update the selectable display by deselecting the stories since they
        # can't be added twice anyway
        self.__selectable_listbox.selection_clear(0, 'end')

        for i in indexes:
            url = self.__selectable_stories[i][0]
            title = self.__selectable_stories[i][4]
            if url not in self.__selected_stories:
                self.__selected_stories.append(url)
                self.__selected_var.append(f'{title} | {url}')
                self.__logger.info(f'Selecting: "{url}"')
            else:
                self.__logger.error(f'Already selected: "{url}"')

            self.__selectable_listbox.itemconfig(i, bg=cst.SELECTED_COLOR)

        self.__logger.debug('URLs selected')
        self.__update_selected_display()

    def __selected_command(self):
        """
        Allow the user to un-select stories
        """
        self.__logger.info('Un-selecting URLs')
        # Reverse the list to avoid any IndexError
        indexes = sorted(self.__selected_listbox.curselection())[::-1]
        # Update the display
        self.__selected_listbox.selection_clear(0, 'end')

        for i in indexes:
            self.__selected_stories.pop(i)
            self.__selected_var.pop(i)

        self.__logger.debug('URLs unselected')
        self.__update_selected_display()
        self.__update_selectable_display()

    def __url_command(self):
        """
        Add the entered URL to the selected stories if it's not already there
        """
        url = self.__url_entered.get().strip()
        self.__logger.info(f'Entering URL: "{url}"')
        self.__url_entered.set('')

        # Update the concerned lists
        if url not in self.__selected_stories and url != '':
            self.__selected_stories.append(url)
            self.__selected_var.append(f'NEW STORY | {url}')

        self.__logger.debug(f'URL "{url}" entered')
        # Update the display
        self.__update_selected_display()

    def __copy_command(self):
        """
        Add the currently selected urls in the selected_listbox to the clipboard
        Delete the previous clipboard
        """
        self.__logger.info('Copying URLs')
        self.__master.clipboard_clear()

        indexes = sorted(self.__selected_listbox.curselection())
        self.__selected_listbox.selection_clear(0, 'end')

        for i in range(len(self.__selected_stories)):
            url = self.__selected_stories[i]
            if i in indexes:
                self.__master.clipboard_append(f'{url}\n')
                self.__selected_var[i] = f'Added to clipboard | {url}'
            else:
                self.__selected_var[i] = f'Not in clipboard | {url}'

        self.__logger.debug('URLs copied')
        self.__update_selected_display()

    def __handle_stories(self, mode: str):
        """
        Can download, update or download the informations for the stories in
        the selected list

        :param mode: 'download', 'update' or 'informations'
        """

        # Prepare the functions to use
        if mode == 'download':
            self.__logger.info(f'Downloading stories')
            writer_func = self.__writer.download
        elif mode == 'informations':
            self.__logger.info('Updating informations')
            writer_func = self.__writer.write_informations
        # Default mode is update since its the most convenient one
        else:
            self.__logger.info('Updating stories')
            writer_func = self.__writer.update

        # The error message must adapt to the different failures
        err_message = 'FAILURE | {} | Reason: {}'

        urls = self.__database.get_column('url', False)

        for i, url in enumerate(self.__selected_stories):

            self.__logger.info(f'Handling URL [{i}]: "{url}"')

            # Tries to both setup the URL and do the wanted action
            try:
                # Setup the story
                self.__writer.set_url(url)

                # Get the correct URL for the story and save it, ensuring the
                # URL-based actions will work (like marking as read or adding to
                # a series)
                new_url = self.__writer.story.url
                self.__selected_stories[i] = new_url

                # Special handling of the situation where the url has never been
                # saved and the user want only download the informations for it
                if mode == 'informations' and new_url not in urls:
                    self.__selected_var[i] = err_message.format(
                        new_url,
                        'No informations to update, story was never downloaded'
                    )
                    self.__logger.error('No informations to update')
                else:
                    # Ensure the story exists in the database even when
                    # not downloaded/updated completely. It will allow the user
                    # to update the story if it fails mid-download
                    self.__database.add_story(self.__writer.story)
                    # Use the prepared function
                    writer_func()
                    self.__selected_var[i] = f'Success | {new_url}'
                    self.__logger.info(f'{mode.title()}: successful')
            # Handles all the errors I thought could happen
            except IndexError as err:
                self.__selected_var[i] = err_message.format(
                    url,
                    f'IndexError: {err}',
                )
                self.__logger.error(f'IndexError: {err}')
            except AttributeError as err:
                self.__selected_var[i] = err_message.format(url, 'Invalid URL')
                self.__logger.error(f'Invalid URL: {err}')
            except (urllib.error.HTTPError, urllib.error.URLError) as err:
                self.__selected_var[i] = err_message.format(url, err.reason)
                self.__logger.error(f'{type(err)}: {err.reason}')
            except (ConnectionError, OSError) as err:
                self.__selected_var[i] = err_message.format(
                    url,
                    f'{type(err)}: {err}'
                )
                self.__logger.error(f'{type(err)}: {err}')
            finally:
                self.__logger.debug(f'Handled URL [{i}]: "{url}"')
                self.__update_display(i)

    def __delete_stories(self):
        """
        Delete the selected stories
        """
        for i, url in enumerate(self.__selected_stories):
            self.__logger.info(f'Deleting story: "{url}"')
            # Delete the story folder if necessary
            paths = self.__database.get_value_by_url('path_to_index', url)
            try:
                path = paths[0].rsplit('/', 1)[0]
                for file in os.listdir(path):
                    os.remove(f'{path}/{file}')
                os.rmdir(path)
                # Delete the entry in the database
                self.__database.delete_story(url)
                self.__selected_var[i] = f'Deleted | {url}'
                self.__logger.debug('Story deleted')
            except (IndexError, FileNotFoundError):
                self.__selected_var[i] = f'URL not present in database | {url}'
                self.__logger.error('Story is not present in database')
            finally:
                self.__update_display(i)

    def __do_statistics(self, site: str):
        """
        Compile the statistics for a specific site. In case the user has not
        downloaded any stories for the site, no statistics are done

        :param site: the site to compile the statistics for
        """
        self.__logger.info(f'Compiling statistics for "{site}"')

        text = ''

        saved_series = self.__database.get_column('series',
                                                  True,
                                                  f'site="{site}"')
        infos = {
            'authors': len(
                self.__database.get_column('author', True, f'site="{site}"')
            ),
            'universes': len(
                self.__database.get_column('universe', True, f'site="{site}"')
            ),
            'chapters': sum(self.__database.get_column('chapter_count',
                                                       False,
                                                       f'site="{site}"'
                                                       )),
            'words': sum(self.__database.get_column('word_count',
                                                    False,
                                                    f'site="{site}"'
                                                    )),
            'read': 0,
            'unread': 0,
            'series': len(saved_series) - (1 if '' in saved_series else 0),
        }

        for i, story in enumerate(self.__database.get_stories_by_site(site)):

            self.__logger.debug(f'Adding "{story[0]} to the statistics"')

            series = '-' if story[13] == '' else f'{story[13]}: n° {story[14]}'
            # Completed story or not ?
            status = '<span class="{}">{}</span>'.format(
                # The classes we want are either 'progress' or 'complete'
                story[7].lower().replace('in ', ''),
                # Either 'In Progress' or 'Complete'
                story[7].title(),
            )
            # Has the story been read ?
            if bool(story[12]):
                read = '<span class="read">Read</span>'
                infos['read'] += 1
            else:
                read = '<span class="unread">Unread</span>'
                infos['unread'] += 1

            text += cst.SITE_STATISTICS_TR_TEMPLATE.format(
                story=story,
                num=i,
                read=read,
                status=status,
                series=series,
            )

            self.__logger.debug('Added')

        self.__logger.debug('Compiled')

        # No need to write anything then because there are no saved stories
        # for the selected site
        if text == '':
            self.__logger.error('No stories saved for this site')
            return

        self.__logger.debug('Writing statistics css')
        with open('0/css/statistics_style.css', 'w', encoding='utf-8') as f:
            f.write(cst.STATISTICS_CSS)

        self.__logger.debug('Writing javascript')
        with open('0/js/sorting.js', 'w', encoding='utf-8') as f:
            f.write(cst.STATISTICS_JS)

        self.__logger.debug('Writing statistics')
        with open(f'{site}_statistics.html', 'w', encoding='utf-8') as f:
            f.write(cst.SITE_STATISTICS_TEMPLATE.format(
                site=site,
                authors=infos['authors'],
                universes=infos['universes'],
                chapters=infos['chapters'],
                words=infos['words'],
                stories=infos['read'] + infos['unread'],
                read=infos['read'],
                unread=infos['unread'],
                series=infos['series'],
                content=text,
            ))

        self.__logger.debug('Statistics written')

    def __each_site_statistics(self):
        """
        Compile the statistics for each handled site
        """
        for site in cst.SITES.keys():
            self.__do_statistics(site)

    # TODO: Decides how the general statistics will look
    # TODO: ensure this function is efficient (not too many SQL calls)
    def __general_statistics(self, *args):
        """
        Compile the general statistics (include all the sites)
        """
        raise NotImplementedError

    def __read_or_unread(self, mode: str):
        """
        Mark the selected stories as read or unread
        :param mode: 'read' or 'unread'
        """
        self.__logger.info(f'Marking selected stories as "{mode.title()}"')
        urls = self.__database.get_column('url')
        for i, url in enumerate(self.__selected_stories):
            if url not in urls:
                self.__selected_var[i] = 'COULD NOT MARK AS {} | {}'.format(
                    mode.upper(),
                    url
                )
                self.__logger.debug(
                    f'"{url}" not saved: could not mark as "{mode.lower()}"'
                )
            else:
                self.__database.update_by_url('read',
                                              mode.lower() == 'read',
                                              url)
                self.__selected_var[i] = f'Marked as {mode.lower()} | {url}'
                self.__logger.debug(f'"{url}" marked as "{mode.lower()}"')

            self.__update_display(i)

    def __add_to_series(self):
        """
        Add the selected stories to a series via a popup which allows the user
        to create series on the spot
        """
        self.__logger.info('Adding selected stories to a series')

        # Get the already existing series from the database
        existing_series = self.__database.get_column('series', True)

        def series_box_command():

            series = series_var.get()
            series_box.selection_clear()

            urls = self.__database.get_column('url')
            for i, url in enumerate(self.__selected_stories):

                # Ensure the url exists in the database
                if url not in urls:
                    self.__selected_var[i] = f'NON DOWNLOADED STORY | {url}'
                    self.__logger.error(f'"{url}" not present in database')
                    continue

                # Check if the url is already present in the series
                urls_in_series = self.__database.get_urls_by_series(series)
                if url in urls_in_series:
                    self.__selected_var[i] = f"Already in '{series}' | {url}"
                    self.__logger.info(f'"{url} already in "{series}"')
                    continue

                # The position in the series
                pos = 0 if series == '' else len(urls_in_series) + 1

                # Update all the relevant informations
                self.__database.update_by_url('series', series, url)
                self.__database.update_by_url('position', pos, url)
                self.__selected_var[i] = f"Added to '{series}' in {pos} | {url}"
                self.__logger.info(f'Added "{url}" in "{series}", n° {pos}')

                self.__update_display(i)

        def series_entry_command():

            new = entry_var.get().strip()
            entry_var.set('')

            if new == '':
                self.__logger.error("A series' name cannot be an empty string")
            elif new in existing_series:
                self.__logger.error(f'"{new}" cannot be added')
            else:
                existing_series.insert(1, new)
                series_box['values'] = existing_series
                self.__logger.info(f'"{new}" added to the existing series')

        # Ensure there is only one extra window open
        for window in self.__top_levels:
            window.destroy()

        # Creating a new window
        window = tk.Toplevel(self.__master)
        window.title('Adding to series')

        # Adding to the existing top level windows to ensure its destruction
        # later
        self.__top_levels.append(window)

        # Ensure there is something to work with
        if len(self.__selected_stories) == 0:
            tk.Label(window,
                     text='No selected stories to add to a series.').pack()
            self.__logger.error('No selected stories to add to a series')
            return

        # Creating the informations label

        label = tk.Label(
            window,
            text=(
                '1. Removing all the stories from a series deletes it.\n'
                '2. Stories not present locally will be ignored.\n'
                '3. Stories are added to the series in the order they appear.\n'
                '4. Series created without stories added to them are deleted.'
            )
        )

        # Creating the part to add a series
        l_frame = tk.LabelFrame(window, text='Create a new series')

        entry_var = tk.StringVar()
        series_entry = tk.Entry(l_frame, textvariable=entry_var)
        series_entry.bind('<Return>', lambda _: series_entry_command())

        # Creating the combobox to select the series
        series_var = tk.StringVar()
        series_box = ttk.Combobox(window,
                                  textvariable=series_var,
                                  state='readonly')
        series_box['values'] = sorted(existing_series)
        series_box.bind('<<ComboboxSelected>>', lambda _: series_box_command())

        label.pack(anchor=tk.CENTER)
        l_frame.pack(fill=tk.Y, expand=tk.YES)
        series_entry.pack(fill=tk.Y, expand=tk.YES, anchor=tk.CENTER)
        series_box.pack(fill=tk.Y, expand=tk.YES, anchor=tk.CENTER)

    def __delete_series(self):
        """
        Allow the user to delete a series. Do not delete the associated stories
        """
        def delete_command():

            series_box.selection_clear()
            series = series_var.get()

            self.__logger.info(f'Deleting series "{series}"')

            for url in self.__database.get_urls_by_series(series):
                self.__database.update_by_url('series', '', url)
                self.__database.update_by_url('position', 0, url)

            self.__logger.info('Series deleted')

            self.__update_selectable_display()

        # Get the already existing series from the database
        # Remove the '' series (no series) option from the choice
        existing_series = sorted(self.__database.get_column('series', True))[1:]

        # Ensure there is only one extra window open
        for window in self.__top_levels:
            window.destroy()

        # Creating a new window
        window = tk.Toplevel(self.__master)
        window.title('Deleting series')

        self.__top_levels.append(window)

        # Ensure there is something to work with
        if len(existing_series) == 0:
            tk.Label(window, text='No series to delete').pack()
            return

        # Creating the informations label
        label = tk.Label(window, text='Will not delete the associated stories.')

        # Creating the combobox to select the series
        series_var = tk.StringVar()
        series_box = ttk.Combobox(window,
                                  textvariable=series_var,
                                  state='readonly')
        series_box['values'] = existing_series

        delete_button = tk.Button(window,
                                  text='Delete selected series',
                                  command=delete_command)

        label.pack(anchor=tk.CENTER)
        series_box.pack(fill=tk.Y, expand=tk.YES, anchor=tk.CENTER)
        delete_button.pack(anchor=tk.CENTER)

    def __color_selectable_listbox(self, story) -> str:
        """
        :param story: the list representation of a story (coming from the
        database)
        :return: the appropriate color for the situation
        """
        self.__logger.debug('Choosing appropriate color')

        series = story[-2] != ''

        # If the story is selected, don't change it's color
        if story[0] in self.__selected_stories:
            return cst.SELECTED_COLOR

        # If the story has been read and is in a series (or not, for either)
        if story[-3] == 1:
            return cst.SERIES_READ_COLOR if series else cst.READ_COLOR
        else:
            return cst.SERIES_UNREAD_COLOR if series else cst.UNREAD_COLOR

    def __sort_stories(self, sort_option: str) -> str:
        """
        Sort (in place) the stories from self.__selectable_stories by the
        selected sorting method

        :param sort_option: one of the keys of the cst.SORT_OPTION dictionary
        :return: the text to format for the labels
        """
        self.__logger.info(f'Sorting selectable stories by "{sort_option}"')
        # Get the selected sort
        sort_num, text = cst.SORT_OPTIONS[sort_option]

        # The sort by series is a little different because we must ensure the
        # stories are also sorted by their position in the series
        if sort_num != 13:
            self.__selectable_stories.sort(key=lambda st: st[sort_num])
        else:
            # Sort by position in series first then by series
            self.__selectable_stories.sort(key=lambda st: st[14])
            self.__selectable_stories.sort(key=lambda st: st[13])

        self.__logger.debug('Sorted selectable stories')
        return text

    def __update_selectable_display(self):
        """
        Update the display for the left listbox: the selectable stories
        """
        self.__master.update()
        # The selected site for which to update the display
        site = self.__selected_site.get()
        # Get the selected sort option
        sort_option = self.__selected_sort.get()
        self.__logger.debug(f'Selectable display: "{site}" by "{sort_option}"')

        # Prepare the stories
        self.__selectable_stories = self.__database.get_stories_by_site(site)
        # Sort the stories
        text = self.__sort_stories(sort_option)

        # The labels and the colors to use for them in the listbox
        labels = []
        colors = []

        self.__logger.debug('Selectable display: setup-ing text')
        for story in self.__selectable_stories:
            # The series part is adaptable
            series = f'[{story[13]}: {story[14]}]' if story[13] != '' else ''

            labels.append(text.format(story=story, series=series))
            colors.append(self.__color_selectable_listbox(story))
        self.__logger.debug('Selectable display: text done')

        # Update the values and their colors without moving the position in the
        # list
        self.__logger.debug('Selectable display: coloring')
        tmp_var = tk.StringVar(value=labels)
        self.__selectable_listbox['listvariable'] = tmp_var
        for i, color in enumerate(colors):
            self.__selectable_listbox.itemconfig(i, bg=color)
        self.__logger.debug('Selectable display: coloring done')

        del labels, tmp_var, colors
        self.__master.update()

    def __update_selected_display(self):
        """
        Update the display for the right listbox: the selected stories
        """
        self.__logger.debug('Making selected display')
        self.__master.update()
        tmp = tk.StringVar(value=self.__selected_var)
        self.__selected_listbox['listvariable'] = tmp
        del tmp
        self.__master.update()
        self.__logger.debug('Selected display: done')

    def __update_display(self, i: int):
        """
        Update the display and move the selected_listbox to see what was updated
        :param i: the index to see
        """
        self.__update_selected_display()
        try:
            # To put the story just treated at the top when the window is the
            # smallest, or somewhere in between if its bigger
            self.__selected_listbox.see(i + 30)
        except IndexError:
            # An IndexError means all the remaining stories are already visible
            pass
        self.__update_selectable_display()


if __name__ == '__main__':
    UI.main()
