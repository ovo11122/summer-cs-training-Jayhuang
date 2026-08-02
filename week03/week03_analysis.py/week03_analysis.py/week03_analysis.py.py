import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv("week03_network_flows.csv",encoding = 'utf-8')
# # print(df.head())
# # print(df.columns)
# # print(df.dtypes)
# # print(df.shape)

# protocol_counts = df['protocol'].value_counts()
# print('\n各协议的网络流数量:')
# print(protocol_counts)

# src_ip_counts = df['src_ip'].value_counts()
# print('\n源ip出现次数：')
# print(src_ip_counts)

# dst_ip_counts = df['dst_ip'].value_counts()
# print('\n目标ip出现次数')
# print(dst_ip_counts)

# src_port_counts = df["src_port"].value_counts()
# print("\n源端口出现次数：")
# print(src_port_counts)

# dst_port_counts = df["dst_port"].value_counts()
# print("\n目标端口出现次数：")
# print(dst_port_counts)

##抓包数据流

df = pd.read_csv('week03_packets.csv',encoding = 'utf-8')

protocol_counts = df['Protocol'].value_counts()
print('\n各协议的数据包数量:')
print(protocol_counts)

bars = plt.bar(protocol_counts.index,protocol_counts.values)#存横轴纵轴
plt.bar_label(bars)
plt.title('Protocol Packet Counts')
plt.xlabel('Protocol')
plt.ylabel('Packet Counts')
plt.tight_layout()
plt.savefig('protocol_distribution.png',dpi = 300)
#plt.show()
plt.close()


src_ip_counts = df['Source'].value_counts()
print('\n源ip出现次数：')
print(src_ip_counts)


dst_ip_counts = df['Destination'].value_counts()
print('\n目标ip出现次数：')
print(dst_ip_counts)

src_port_counts = df['src_port'].value_counts()
print('\n源端口出现次数：')
print(src_port_counts)

dst_port_counts = df['dst_port'].value_counts()
print('\n目标端口出现次数：')
print(dst_port_counts)

bars = plt.bar(dst_port_counts.head(10).index,dst_port_counts.head(10).values)
plt.bar_label(bars)
plt.title('Top 10 Destination Ports')
plt.xlabel('Destination Port')
plt.ylabel('Packet Count')
plt.tight_layout()
plt.xticks(rotation=45,ha = 'right')#旋转45度向右对齐
plt.savefig("top_destination_ports.png", dpi=300)
#plt.show()
plt.close()



length_groups = pd.cut(#把数据全都通过bins去分到每个label里
    df['Length'],
    bins = [0,100,500,1000,1500,float('inf')],
    labels = ['0-99',"100-499","500-999","1000-1499","over1500"],
    right = False)
length_distribution = length_groups.value_counts().sort_index()#通过左边0-99等排序而不是大小排序
print(length_distribution)
#print(length_groups) 

bars = plt.bar(length_distribution.index,length_distribution.values)
plt.bar_label(bars)
plt.title("Packet Length Distribution")
plt.xlabel("Packet Length")
plt.ylabel("Packet Count")
plt.tight_layout()
plt.savefig("packet_length_distribution.png", dpi=300)
plt.show()
plt.close()