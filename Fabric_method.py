# Source: https://proglib.io/p/factory-method-python



"""
Допустим, есть задача: сделать класс, который умеет сереализовать
экземпляр класса Song. Этим классом предстает SongSerializer. При
возникновении потребности сериализовать Song не только в формат JSON, но
и в формат XML возникает сложность:
1) Надо реализовывать супер класс который будет обладать методами для
сериализации как в JSON, так и в XML;
2) Можно внутри метода описать ветвление, которое будет зависеть от
передаваемого в метод параметра;
3) Применить практику фабричного метода.
"""


import json
import xml.etree.ElementTree as et

class Song:
    def __init__(self, song_id, title, artist):
        self.song_id = song_id
        self.title = title
        self.artist = artist


class SongSerializerBad:
    def serialize(self, song, format):
        if format == 'JSON':
            song_info = {
                'id': song.song_id,
                'title': song.title,
                'artist': song.artist
            }
            return json.dumps(song_info)
        
        if format == 'XML':
            song_info = et.Element('song', attrib={'id': song.song_id})
            title = et.SubElement(song_info, 'title')
            title.text = song.title
            artist = et.SubElement(song_info, 'artist')
            artist.text = song.artist
            return et.tostring(song_info, encoding='unicode')
        
        raise ValueError(format)


"""
Выше представлен метод serialize, внутри которого и выполняется
ветвление. Способ рабочий, но скрывает под собой множество проблем.
В частности:
1) Структура полей класса Song может измениться, а это за собой повлечет
изменение и реализации метода serialize;
2) Появление нового формата для сериализации также повлечет изменение
метода serialize;
Оба вероятных варианта развития событий, в свою очередь, повлекут
необходимость в изменении unit- тестов для этого метода. Собственно
говоря, куда приятнее добавлять новый функционал, нежели чинить старый.
"""


"""
Проведем рефакторинг класса. Первым делом разделим сущности 
'сериализовать' и 'сериализовать в особый формат':
"""

class SongSerializerWihoutSolidDependecies:
    def serialize(self, song, format):
        if format == 'JSON':
            return self._serialize_to_json(song)
        elif format == 'XML':
            return self._serialize_to_xml(song)
        else:
            raise ValueError(format)

    def _serialize_to_json(self, song):
        payload = {
            'id': song.song_id,
            'title': song.title,
            'artist': song.artist
        }
        return json.dumps(payload)

    def _serialize_to_xml(self, song):
        song_element = et.Element('song', attrib={'id': song.song_id})
        title = et.SubElement(song_element, 'title')
        title.text = song.title
        artist = et.SubElement(song_element, 'artist')
        artist.text = song.artist
        return et.tostring(song_element, encoding='unicode')


"""
Бывшие проблемы были нивилированы. Теперь можно добавлять новые форматы
для сериализации без опаски, что придется переписывать старые тесты, а
также с гарантией, что старый функционал так и остался в прежнем
состоянии.
"""


"""
Базовая реализация фабричного метода в данном контексте выглядит
следующим образом. Метод serialize остается, но внутри него вызывается
другой метод _get_serializer. Этот новый метод на основании переданного
в него парметра format определяет, какую реализацию метода serialize
ожидает использовать пользователь класса. 
"""


"""
Главная идея фабричного метода заключается в следующем: ответственность
за выбор реализации метода ложится на плечи отдельного компонента в
зависимости от передаваемого параметра.
"""


class SongSerializerBasicFabric:
    def serialize(self, song, format):
        serializer = self._get_serializer(format)
        return serializer(song)

    def _get_serializer(self, format):
        if format == 'JSON':
            return self._serialize_to_json
        elif format == 'XML':
            return self._serialize_to_xml
        else:
            raise ValueError(format)

    def _serialize_to_json(self, song):
        payload = {
            'id': song.song_id,
            'title': song.title,
            'artist': song.artist
        }
        return json.dumps(payload)

    def _serialize_to_xml(self, song):
        song_element = et.Element('song', attrib={'id': song.song_id})
        title = et.SubElement(song_element, 'title')
        title.text = song.title
        artist = et.SubElement(song_element, 'artist')
        artist.text = song.artist
        return et.tostring(song_element, encoding='unicode')


"""
В окончательной реализации фабричного метода возможно выделить четыре
компонента:

1) компонент - клиент
2) компонент - создатель
3) компонент - реализация
4) продукт

В данном случае метод serialize является клиентским компонентом,
компонентом создателем является метод _get_serializer. Компонентами
реализациями является два метода, _serialize_to_json и
_serialize_to_xml. Продуктом является экземпляр класса Song.
"""


"""
Можно подметить, что метод фабрика не опирается на использование self.
Таким образом можно провести еще один рефакторинг и вынести всю фабрику
в раздел методов класса.
"""


class SongSerializerStatiocBasicFabric:
    def serialize(song, format):
        serializer = self._get_serializer(format)
        return serializer(song)

    def _get_serializer(format):
        if format == 'JSON':
            return self._serialize_to_json
        elif format == 'XML':
            return self._serialize_to_xml
        else:
            raise ValueError(format)

    def _serialize_to_json(song):
        payload = {
            'id': song.song_id,
            'title': song.title,
            'artist': song.artist
        }
        return json.dumps(payload)

    def _serialize_to_xml(song):
        song_element = et.Element('song', attrib={'id': song.song_id})
        title = et.SubElement(song_element, 'title')
        title.text = song.title
        artist = et.SubElement(song_element, 'artist')
        artist.text = song.artist
        return et.tostring(song_element, encoding='unicode')

"""
Предпосылки к использованию фабричного мтеода:


"""