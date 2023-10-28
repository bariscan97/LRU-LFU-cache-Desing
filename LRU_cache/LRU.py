class LRUCache:

    def __init__(self, capacity: int):
        
        self.dic={}
        self.cap=capacity
    
    def get(self, key: int) -> int:
        
        if key in self.dic:
            val=self.dic[key]
            self.dic.pop(key)
            self.dic[key]=val
            return self.dic[key]
        return -1

    def put(self, key: int, value: int) -> None:
        
        if len(self.dic)==self.cap and not key in self.dic:
           self.dic.pop(next(iter(self.dic)))
        if key in self.dic:self.dic.pop(key)
        self.dic[key]=value   
        
        
        
        

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
