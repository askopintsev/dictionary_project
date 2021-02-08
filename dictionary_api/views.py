from datetime import datetime

from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView

from .models import Dictionary, Element
from .serializers import DictionarySerializer, ElementSerializer


class DictionariesView(ListAPIView):
    """Class provides view to work with Dictionary entities.
    API endpoint: <host>/api/dictionaries/
    Accepts:
        start_date: datetime (expecting format "YYYY-MM-DD")(non-mandatory)
                    - checking date to find actual dictionaries
    Returns:
        if start_date is filled - only dictionaries which are actual for this date/
        else - full list of dictionaries
    """

    serializer_class = DictionarySerializer
    paginate_by = 10

    def get_queryset(self):

        start_date = self.request.query_params.get("start_date")

        # handling filled start_date parameter
        if start_date:
            try:
                start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                raise ValidationError('Incorrect format for start_date parameter. Please use format "YYYY-MM-DD"')

            queryset = Dictionary.objects.raw('''SELECT * FROM dictionary
                                                  WHERE start_date < %s
                                                  GROUP BY name
                                                 HAVING start_date = max(start_date)
                                                  ORDER BY start_date DESC''', [start_date_dt])

        else:
            queryset = Dictionary.objects.all()

        return queryset


class ElementsView(ListAPIView):
    """Class provides view to work with dictionary Elements.
    API endpoint: <host>/api/elements/
    Accepts:
        parent_dict: str (required) - name of dictionary to filter its elements
        version: int (expecting)(non-mandatory) - version of dictionary to filter its elements
        element_code: str (non-mandatory) - code of element to be check for presence in dictionary
    Returns:
        list of dictionary elements filtered by dictionary name
        from actual version of dictionary (if version parameter was empty)
        or from selected version of dictionary (if version parameter was filled)
        if element_code was set - it returns this element as flag of its presence in dictionary
    """

    serializer_class = ElementSerializer
    paginate_by = 10

    def get_queryset(self):

        # handling parent_dict parameter
        parent_name = self.request.query_params.get("parent_dict")
        if parent_name is None:
            raise ValidationError(
                'Empty value for required parent_dict parameter. Please fill value with name of the dictionary.'
            )

        # getting non-mandatory parameters
        version = self.request.query_params.get("version")
        element_code = self.request.query_params.get("element_code")

        # setting base for query
        query_string = '''SELECT e.id, element_code, value 
                            FROM element e
                            JOIN element_parent ep on e.id = ep.element_id
                            JOIN dictionary d on d.id = ep.dictionary_id
                           WHERE d.name = %s'''
        arguments = [parent_name]

        # handling version parameter
        if version:
            query_string += 'AND d.version = %s'
            arguments.append(version)
        else:
            query_string += '''AND d.version = (SELECT max(version) 
                                                  FROM dictionary 
                                                 WHERE name = %s 
                                                 GROUP BY name)'''
            arguments.append(parent_name)

        # handling element_code parameter
        if element_code:
            query_string += 'AND element_code = %s'
            arguments.append(element_code)

        # making call to DB
        queryset = Element.objects.raw(query_string, arguments)

        return queryset
