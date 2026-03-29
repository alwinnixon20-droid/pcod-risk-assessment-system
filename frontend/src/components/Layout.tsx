import { Outlet, NavLink } from "react-router-dom";

export default function Layout() {
  return (
    <div style={{ display: "flex" }}>
      
      <div style={{ width: "200px", padding: "20px", background: "#f0f0f0" }}>
        <h2>PCOS App</h2>

        <nav style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
          <NavLink to="/predict">Predict</NavLink>
        </nav>
      </div>

      <div style={{ flex: 1, padding: "20px" }}>
        <Outlet />
      </div>

    </div>
  );
}