import os

#f = open("list.txt","a",encoding="utf-8")


#the plan:
#do os.walk() and collect names and paths of all files
#check size of every file https://www.digitalocean.com/community/tutorials/how-to-get-file-size-in-python 
#hash every file https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
#find duplicating files 

foundFilesList=list()#list of dictionaries containing details of every found file
counterFolders=0
limit=1000000



cwd=os.getcwd()
print(f"current working directory: {cwd}")

for root, dirs, files in os.walk('.'):#os.walk() returns a generator, that creates a tuple of values
    #print(f"root: {root}, dirs: {dirs}, files: {files}")
    rootStrNormalized=os.path.normpath(root)#example root='./.git/logs' rootStrNormalized='.git/logs'
    rootSplited=rootStrNormalized.split(os.sep)#example rootStrNormalized='.git/logs' rootSplited=['.git', 'logs']
    folder=rootSplited[-1]#in this folder you are only the deepest folder, no full path
    counterFolders+=1
    for file in files:
        #print(file)
        file_name, file_extension = os.path.splitext(file)
        file_extension =file_extension.replace('.','')
        root=root.replace('.',cwd)
        #f.write(root+","+folder+","+file+","+file_extension+"\n")
        nextFile={"root":root, "folder":folder, "filename":file, "extension":file_extension}
        print(nextFile)(
        foundFilesList.append(nextFile)
        if(len(foundFilesList) >= limit):
            print("too much, stopping now")
            break
        
print(str(len(foundFilesList))+ " files found in " + str(counterFolders)+ " folders")
        
#f.close()
