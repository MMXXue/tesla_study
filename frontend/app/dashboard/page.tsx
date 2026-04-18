
import {ItemsStatusCard} from "../components/ItemsStatusCard";


export default function DashBoard(){
    const device = [
        {deviceId: "1111", status: 'In progress', healthy: "93", temperature: "90", battery: "85"},
        {deviceId: "2222", status: 'Error', healthy: "100", temperature: "105", battery: "30"},
    ];

    return (
        <main>
            <h1 className="text-2xl font-light m-10 tracking-widest uppercase">
                工厂资产管理面板
            </h1>
            <div className="bg-grey p-6">
                {device.map(item => (
                    <ItemsStatusCard 
                        key={item.deviceId}      // 这是给 React 用的，消灭那个 unique key 警告
                        deviceId={item.deviceId} // 这是传给组件内部用的，消灭现在这个 TS 报错
                        status = {item.status as any}
                        healthy = {item.healthy}
                        temperature = {item.temperature}
                        battery = {item.battery} 
                    />
                ))}
            </div>
        </main>
    );
}