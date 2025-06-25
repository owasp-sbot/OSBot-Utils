# todo: create this readme based on the current files in this folder

### Bugs and Feature requests

 - see if we can prevent new fields from being added in the ctor

for example 

```File_FS__Content(file__config=file_config, storage=self.storage)```

and 

```File_FS__Content(file_config=file_config, storage=self.storage)```

works with 

```
class File_FS__Content(File_FS):
    file__config : Schema__Memory_FS__File__Config
    storage      : Memory_FS__Storage
```

the problem is that the 2nd will create a new variable called ```file_config```(vs the correct 
```file__config```), which has not been defined and (as happened in this case), can introduce bugs
In the past we did some experiments on the idea of 'freezing' the class which at the time was implemented
using an extra __locked__ (or similar), this was early days of Type_Safe with much lower test coverage
and defined use cases. Now with the focus being on runtime type safety, there is a case
for not allowing new fields from being added to a class (which in a way break type safety)