import {createBrowserRouter} from "react-router-dom";
import Layout from "./components/Layout/Layout";
import Projects from "./pages/Projects";
import Menu from "./pages/Menu";
import RegLoginPage from "./pages/RegPage";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <Layout/>,
        children: [
            {
                path: "/",
                element: <RegLoginPage/>
            },
            {
                path: "/projects/",
                element: <Projects/>
            },
            {
                path: "/menu/",
                element:<Menu/>
            },
            {
                path: "/tasks/",
                element:<Menu/>
            }
        ]
            
    }
])