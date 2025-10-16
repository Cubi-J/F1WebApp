export default function DriverCard({ driver }){
  return (
    <div className="flex flex-col rounded-xl overflow-hidden shadow-md p-0 hover:shadow-xl hover:-translate-y-1 dark:hover:shadow-gray-700 transition-all duration-300">
      <div className="aspect-square rounded-t-xl flex items-center justify-center">
        <img
          src={driver.headshot_url}
          alt={driver.full_name}
          className="w-full h-full object-cover mx-auto shadow-md"
          style={{ backgroundColor: `#${driver.team_color}` }}
        />
      </div>
      <div className="p-4 rounded-b-xl flex-1 bg-white dark:bg-gray-900">
        <h2 className="text-lg font-bold dark:text-white">{driver.first_name}</h2>
        <h2 className="text-lg font-bold dark:text-white">{driver.last_name}</h2>
        <p className="dark:text-gray-100 text-gray-900">{driver.team_name}</p>
      </div>
    </div>
  );
}