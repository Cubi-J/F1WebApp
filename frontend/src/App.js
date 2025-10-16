import NextRaceCard from "./components/NextRaceCard";
import Drivers from "./pages/Drivers";

function App() {
  return (
    <div className="bg-gray-100 dark:bg-gray-600 text-center p-10">
      <h1 className="text-3xl font-bold text-red-600 dark:text-blue-500">
        FastF1 WebApp
      </h1>
      <NextRaceCard />
      <Drivers />
    </div>
  );
}



export default App;
