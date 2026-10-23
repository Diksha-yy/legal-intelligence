import AppRoutes from "./routes/AppRoutes";
import { AuthProvider } from "./context/AuthContext";
import { MotionConfig } from "framer-motion";

function App() {
  return (
    <MotionConfig reducedMotion="user">
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </MotionConfig>
  );
}

export default App;
