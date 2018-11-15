#!/usr/bin/env python
# coding=utf-8

from rest_framework import serializers
# from rest_framework.utils import model_meta
# from rest_framework.compat import set_many


"""
def update_instance(instance, validated_data):
    info = model_meta.get_field_info(instance)
    for attr, value in validated_data.items():
        if attr in info.relations and info.relations[attr].to_many:
            set_many(instance, attr, value)
        else:
            setattr(instance, attr, value)
    instance.save()
    return instance
"""


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            header = None
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(header, file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

            # print('data: %s', data)
        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, header, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        if not extension:
            extension = header.split('/')[-1]

        extension = "jpg" if extension == "jpeg" else extension
        return extension


class Base64FileField(serializers.FileField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            header = None
            # Check if the base64 string is in the "data:" format data:mov;base64,
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, header)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

            # print('data: %s', data)
        return super(Base64FileField, self).to_internal_value(data)

    def get_file_extension(self, file_name, header):
        # extension = imghdr.what(file_name, decoded_file)
        # extension = "jpg" if extension == "jpeg" else extension
        extension = header.strip().split(':')[-1]

        return extension


##############################
# 列表更新操作
##############################
class CustomListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        return super(CustomListSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        queryset = self.context.get('queryset', None)
        del_no_in_list = self.context.get('del_no_in_list', False)

        if queryset:
            instance_mapping = {item.id: item for item in queryset}
            if del_no_in_list:
                data_ids = [item['id'] for item in validated_data]
                for instance_id, instance_data in instance_mapping.items():
                    if instance_id not in data_ids:
                        instance_data.delete()
        else:
            instance_mapping = None

        ret = []

        foreign_keys = self.context.get('foreign_keys', None)
        for idx, data_item in enumerate(validated_data):
            pk = data_item.pop('id', -1)
            if not data_item:
                continue

            if foreign_keys:
                for foreign_key in foreign_keys:
                    data_item[foreign_key] = self.context[foreign_key]

            if pk == -1:
                ret.append(self.child.create(data_item))
                continue

            data_instance = None if instance_mapping is None else instance_mapping.get(pk, None)
            if data_instance is None:
                ret.append(self.child.create(data_item))
            else:
                ret.append(self.child.update(data_instance, data_item))
        return ret
