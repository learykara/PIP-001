import forgery_py

from tuneful.models import File, Song


def seed_db():
    for x in range(10):
        filename = forgery_py.lorem_ipsum.word()
        file = File(filename='{}.mp3'.format(filename)).save()
        Song(file_id=file.id).save()


if __name__ == '__main__':
    seed_db()
