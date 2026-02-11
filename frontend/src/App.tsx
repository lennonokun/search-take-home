import { SearchPage } from "./features/search/SearchPage";
import { NotepadStream } from "./features/streaming/NotepadStream";

function App() {
  return (
    <div
      style={{ maxWidth: 800, margin: "2rem auto", fontFamily: "system-ui" }}
    >
      <h1>Search Demo</h1>
      <SearchPage />
      <NotepadStream />
    </div>
  );
}

export default App;
