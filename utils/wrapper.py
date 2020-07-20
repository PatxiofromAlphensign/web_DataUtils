import argparse
import os
import numpy as np

"""
TODO: simplify and add abstract strcutre using other liberies such as numpy and pandas. Construct a torch dataset with ranged download of files from s3
"""

class pathloader_base:
    """
        constructs iterable over all the paths across the range of files in `path` 
    """
    def __init__(self,path):
        self.path = path
        self.all_lines = []
        for fi in os.listdir(path):
            with open(os.path.join(path,fi), 'r') as r:
                self.all_lines.append(r.readlines())
    
    @property
    def label_configs(self):
        return ['000', '2020'] 

    def generalize_labels_into_ids(self,q):
        "returns q idx on each row "
        
        self.sc = []
        for k in self.all_lines:
            pair = []
            # the pairs that are commnon
            for i,x in enumerate(k[0].split('/')):
                if q in x:
                    self.sc.append(i)
                    break
        
        return self.sc            
    
    def ReallabelsDict(self):
        labels = {}
        for val in self.label_configs:
            for data,idx in zip(self.all_lines, self.generalize_labels_into_ids(val)):
                
                for d in data[:10]:
                    labels[d.split('/')[idx]] =idx
    
        return labels



class PathLoader(pathloader_base):
    def __init__(self, path):
        "" 
        super(PathLoader, self).__init__(path)
        self.labelidx = []
        for q in self.label_configs:
            self.labelidx.append(self.generalize_labels_into_ids(q))
        
        #reshape(len(self.labelidx[0])*len(self.labelidx[1]))
        self.asfull = np.array(self.labelidx).reshape(len(self.labelidx[0])*len(self.labelidx[1]))
    
    def __getitem__(self, key):
        return self.all_lines[key]
            
    def listByidx(self, query)->list:
        """
            query by index 
        """
        itr = []
        for batch in self.all_lines:
            for i,k in enumerate(batch):

                label_idx = self.split_cat()[0]['cdx-00000.gz\n']
                if query in k.split('/')[-1]:
                    itr.append(batch[i])
        return itr

    def listByhdate(self, query)->list:
        """
            query by bydate 
        """
        itr = []
        for c,batch in enumerate(self.all_lines):
            for i,k in enumerate(batch):
                label_idx = self.split_cat()[0]['CC-MAIN-2020-24']

                if query in k.split('/')[label_idx]:
                    itr.append(batch[i])
        return itr



def querywithmaxrange(path,query, max_range):
    idx = path.list_byidx(query)[:max_range] 
    return idx
   #return path.map2dict()

def autobatched_dataset(path_list):

    for path in path_list:
        path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir',help='dir' ,default='data', type=str)
    parser.add_argument('--list',help='list', type=str)
    args = parser.parse_args()

    path = PathLoader(args.dir)
    print(path.asfull)


    #print((namesbyrange(path, 111)))

