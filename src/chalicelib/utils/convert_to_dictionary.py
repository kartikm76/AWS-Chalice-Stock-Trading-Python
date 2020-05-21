class ConvertToDictionary:
    
    @classmethod
    def convert_to_dictionary(self, obj):
        self.obj = obj
        obj_dict = {}
        # Populate the dictionary with object properties
        obj_dict.update(self.obj.__dict__)
        return obj_dict