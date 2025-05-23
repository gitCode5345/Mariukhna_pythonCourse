def check_list_size(func):
    def wrapper(self, *args, **kwargs):
        if not self.copy_list or not self.init_list or not self.genres:
            print('Data missing')
            return None
        return func(self, *args, **kwargs)
    return wrapper

