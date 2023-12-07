# from .models import User_Details
# from .serializers import UserSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import pandas as pd
# import hashlib

# def fingerprint(value, secret_key):
#     data_to_hash = f"{value}{secret_key}".encode('utf-8')
#     hashed_value = hashlib.sha256(data_to_hash).hexdigest()
#     fingerprint_value = int(hashed_value, 16)
#     return fingerprint_value

# class UploadCSVView(APIView):
#     SECRET_KEYS = {
#         'name': 'secret_key_name',
#         'age': 'secret_key_age',
#         'occupation': 'secret_key_occupation',
#         'sex': 'secret_key_sex',
#         'maritalStatus': 'secret_key_maritalStatus',
#         'race': 'secret_key_race',
#         'education': 'secret_key_education',
#     }
#     def post(self, request, *args, **kwargs):
#         uploaded_file = request.FILES['file']
#         df = pd.read_csv(uploaded_file)
        
#         for column in ['name', 'occupation', 'sex', 'maritalStatus', 'race', 'education']:
#             df[column] = df[column].astype('category').cat.codes
#         fingerprinted_data = []
#         MAX_INT64 = 9223372036854775807 

#         for column in self.SECRET_KEYS:
#             df[f'fingerprint_{column}'] = df[column].apply(lambda x: fingerprint(x, self.SECRET_KEYS[column])% MAX_INT64)
#             print(df[f'fingerprint_{column}'])
#         User_Details.objects.bulk_create([User_Details(**row) for row in df.to_dict(orient='records')])
#         mean_values = df.mean().to_dict()

#         return Response({
#             'message': 'Data uploaded and processed successfully',
#             'mean_values': mean_values
#         }, status=status.HTTP_201_CREATED)




from .models import User_Details
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import numpy as np

class UploadCSVView(APIView):
    SECRET_KEYS = {
        'name': 'secret_key_name',
        'age': 'secret_key_age',
        'occupation': 'secret_key_occupation',
        'sex': 'secret_key_sex',
        'maritalStatus': 'secret_key_maritalStatus',
        'race': 'secret_key_race',
        'education': 'secret_key_education',
    }

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES['file']
        df = pd.read_csv(uploaded_file)

        # Add a new column 'random_sequence' with random sequence numbers to the DataFrame
        # df['random_sequence'] = np.random.permutation(len(df)) + 1

        L = 1
        y = 2

        for column in ['occupation', 'sex', 'maritalStatus', 'race', 'education']:
            df[column] = df[column].astype('category').cat.codes
        for column in ['name', 'age']:
            df[column] = df[column].astype('category').cat.codes
            df[f'fingerprint_{column}'] = df.apply(lambda row: self.modify_fingerprint_column(row['id'], row[column], L, y), axis=1)

        User_Details.objects.bulk_create([User_Details(**row) for row in df.to_dict(orient='records')])
        
        # Calculate mean values for 'name', 'age', 'fingerprint_name', 'fingerprint_age'
        mean_values = df[['name', 'age', 'fingerprint_name', 'fingerprint_age']].mean().to_dict()

        return Response({
            'message': 'Data uploaded and processed successfully',
            'mean_values': mean_values
        }, status=status.HTTP_201_CREATED)

    # def post(self, request, *args, **kwargs):
    #     uploaded_file = request.FILES['file']
    #     df = pd.read_csv(uploaded_file)
        
    #     # Add a new column 'random_sequence' with random sequence numbers to the DataFrame
    #     #df['random_sequence'] = np.random.permutation(len(df)) + 1

    #     L = 1
    #     y = 2

    #     for column in ['occupation','sex','maritalStatus','race','education']:
    #         df[column] = df[column].astype('category').cat.codes
    #     for column in ['name', 'age']:
    #         df[column] = df[column].astype('category').cat.codes
    #         df[f'fingerprint_{column}'] = df.apply(lambda row: self.modify_fingerprint_column(row['id'], row[column], L, y), axis=1)


    #     User_Details.objects.bulk_create([User_Details(**row) for row in df.to_dict(orient='records')])
    #     mean_values = df.mean().to_dict()

    #     return Response({
    #         'message': 'Data uploaded and processed successfully',
    #         'mean_values': mean_values
    #     }, status=status.HTTP_201_CREATED)

    def modify_fingerprint_column(self, primary, value, L, y):
        hashed_value = primary
        
        # Extracting components from the fingerprint value
        v = 7  # Example value, you may need to adjust it based on your requirements
        i = primary % v
        j = primary % 7  # Assuming § = 7, you may need to adjust it based on your requirements
        l = primary % L
        
        if (primary % y) == 0:
            # Applying the described logic
            attribute_index_i = i
            bit_index_j = j
            mask_bit_x = 0 if (primary % 2) == 0 else 1
            fingerprint_index_l = l
            fingerprint_bit_f = value & 1  # Extracting the least significant bit
            mark_bit_m = fingerprint_bit_f ^ mask_bit_x

            # Set the least significant bit j of attribute value to mark_bit_m
            value = (value & ~(1 << j)) | (mark_bit_m << j)
            return (value)
        
        return int(value)  # Returning None if the condition is not met