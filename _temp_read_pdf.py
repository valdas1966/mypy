from f_google.services.drive import Drive

drive = Drive.Factory.valdas()

path = '2026/03/Heuristic_search_for_one_to_many_shortest_path_queries (3).pdf'

# Download to local disk so Claude can read it
drive.download(path_src=path,
               path_dest='/Users/eyalberkovich/mypy/_temp_article.pdf')
print("Downloaded successfully!")
