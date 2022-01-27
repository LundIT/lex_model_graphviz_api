input_json_1 = {
            'models':{
                'class1': {
                    'columns': [
                    {'column_name': 'id', 'data_type': 'FloatField', 'default_value': None},
                    {'column_name': 'c1', 'data_type': 'FloatField', 'default_value': 0},
                    {'column_name': 'c2', 'data_type': 'XLSXField', 'default_value': None},
                    ],
                    'settings': {'is_calculatable': True, 'file_path': 'UploadFiles.GeneralFiles', 'defining_fields': ['c1', 'c2']}
                },
                'class2': {'columns':[
                    {'column_name': 'id', 'data_type': 'FloatField', 'default_value': None},
                    {'column_name': 'c3', 'data_type': 'ForeignKey', 'default_value': None, 'to': 'class1', 'on_delete': 'CASCADE'},
                ], 'settings': {'is_upload_model': True, 'file_path': 'UploadFiles.SpecificFiles'}
                }
            },
            'settings': {'project_name': 'TestGitRepoCreation', 'github_repository': 'https://docker_lex_azure:0a102e14b10e52be18d87a2fb8556aa136e163e3@github.com/LundIT/TestGitRepoCreation.git'}
        }