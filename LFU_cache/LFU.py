from sortedcontainers import SortedDict
class LFUCache:

    def __init__(self, capacity: int):
        self.capacity=capacity
        self.map=defaultdict(OrderedDict)
        self.dic=defaultdict(OrderedDict)
        self.res=SortedDict()
    def get(self, key: int) -> int:
        if not key in self.dic:return -1
        item=self.map[key]
        self.map[key]+=1
        self.res[item].pop(key)
        if self.res[item]=={}:self.res.pop(item)
        if self.map[key] in self.res:self.res[self.map[key]][key]=""
        else:self.res[self.map[key]]={key:""}
        return self.dic[key]
    def put(self, key: int, value: int) -> None:
        if len(self.dic)==self.capacity and not key in self.dic:
            ind=next(iter(self.res))
            item=next(iter(self.res[ind]))
            self.res[ind].pop(item)
            if self.res[ind]=={}:self.res.pop(ind)
            self.map.pop(item)
            self.dic.pop(item)
        self.dic[key]=value
        if key in self.map:
            item=self.map[key]
            self.map.pop(key)
            self.map[key]=item+1
            self.res[item].pop(key)
            if self.res[item]=={}:self.res.pop(item)
            if item+1 in self.res:
                if self.res[item+1].get(key)!=None:self.res[item+1].pop(key)
                self.res[item+1][key]=""
            else:self.res[item+1]={key:""}
        else:
            self.map[key]=1
            if 1 in self.res:
                if key in self.res[1]:self.res[1].pop(key)
                self.res[1][key]=""
            else:self.res[1]={key:""}
        
        
        
# Your LFUCache object will be instantiated and called as such:
# obj = LFUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
