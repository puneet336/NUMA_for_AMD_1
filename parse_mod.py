import os
import subprocess
import re
from shutil import copyfile
import fileinput
from collections import OrderedDict


result1=subprocess.run(['hwloc-ls'],stdout=subprocess.PIPE)
result2=subprocess.run(['numactl', '-H'],stdout=subprocess.PIPE)

_dict1=OrderedDict()
_dict2=OrderedDict()
_data1=result1.stdout.decode('utf-8').split('\n')
_data2=result2.stdout.decode('utf-8').split('\n')

_index=0
_max_index=len(_data1)


def createtemplate(dict1,dict2):
    with open('appfile.sh','w') as _file:
        for k,v in dict1.items():
            _file.write ("-np 1 ./"+k+'.sh\n')
    
    for k,v in dict1.items():
        copyfile('xhpl_template.sh', k+'.sh')
        with fileinput.FileInput(k+'.sh', inplace=True, backup='.bak') as _file:
            for line in _file:
                print(line.replace("COREID_COMMA", v[0]), end='') 
        with fileinput.FileInput(k+'.sh', inplace=True, backup='.bak') as _file:
            for line in _file:
                print(line.replace("MEMORY_CHANNEL",str(v[1])),end='')

    for k,v in dict2.items():
        with fileinput.FileInput(k+".sh",inplace=True,backup=".bak") as _file:
            for line in _file:
                print(line.replace("COREID_SPACE",v),end="")

         

def getcores():
    pass



while True:
#    print("L3:"+str(_index)+""+_data[_index])
    _numa_counter=-1
    _numa_node_number=0
    if re.match(".* Package .*",_data1[_index]):
        p_key= _data1[_index].split("#")[1]
        _index=_index+1
        while True:
            if re.match(".* NUMANode .*",_data1[_index]):
                _index=_index+1
                #L3 is followed by NUMA Node
                while True:
                    if re.match(".*  L3 .*",_data1[_index]): 
                        _numa_counter=_numa_counter+1
                        if _numa_counter == 2:
                            _numa_node_number=_numa_node_number+1
                            _numa_counter=0
                        _index=_index+1
                        _core_id=""
                        while True:
                            if re.match(".* L2 .*",_data1[_index]):
                                _core_id=_core_id+","+_data1[_index].split('#')[-1].split(')')[0]
                                _index=_index+1
                            else:
                                _core_id=_core_id[1:]
                                _key="p"+str(p_key)+"n"+str(_numa_node_number)+"ccx"+str(_numa_counter)
                                _dict1[_key]=[_core_id]
                                _pattern_core_id=re.sub(",",".*",_core_id.strip())
                                _core_id=re.sub(","," ",_core_id)
                                _pattern_core_id="^node.*"+_pattern_core_id+".*"
                                for _line1 in _data2:
                                    if re.match(_pattern_core_id,_line1):
                                       _dict1[_key].append( _line1.split()[1])
                                         
                                _dict2[_key]=_core_id
                                break
                    else:
                        break        
                #Numa Node followed by L2
                if re.match(".* NUMANode .*",_data1[_index]):     
                   continue

                #L2 is followed by NUMA Node
                if re.match(".*  L2 .*",_data1[_index]):
                    _numa_counter=_numa_counter+1
                    if _numa_counter == 2:
                        _numa_node_number=_numa_node_number+1
                        _numa_counter=0
                    _core_id=""
                    while True:
                        if re.match(".* L2 .*",_data1[_index]):
                            _core_id=_core_id+","+_data1[_index].split('#')[-1].split(')')[0]
                            _index=_index+1
                        else:
                            _core_id=_core_id[1:]
                            _key="p"+str(p_key)+"n"+str(_numa_node_number)+"ccx"+str(_numa_counter)
                            _dict1[_key]=[_core_id]
                            _pattern_core_id=re.sub(",",".*",_core_id.strip())
                            _core_id=re.sub(","," ",_core_id)
                            _pattern_core_id="^node.*"+_pattern_core_id+".*"
                            for _line1 in _data2:
                                if re.match(_pattern_core_id,_line1):
                                    _dict1[_key].append( _line1.split()[1])
                            _dict2[_key]=_core_id
                            break     
                    #NUMA Node is followed by L2, let's process it via outer loop
                    if re.match(".* NUMANode .*",_data1[_index]):
                        continue
            if re.match(".* Package .*",_data1[_index]):
                _index=_index-1
                break
            
            _index=_index+1
            if _index  > _max_index-1:
                createtemplate(_dict1,_dict2)
                exit(2)
    _index=_index+1
    if _index  > _max_index-1:
        createtemplate(_dict1,_dict2)
        exit(3)

