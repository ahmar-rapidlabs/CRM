import useAuth from "./useAuth"
import useAxiosPrivate from "./usePrivate"

export default function useUser() {

    const { isLoggedIn, setUser } = useAuth()
    const axiosPrivateInstance = useAxiosPrivate()

    async function getUser() {
        if (!isLoggedIn) {
            return
        }

        try {
            const { event } = await axiosPrivateInstance.get('auth/')
            console.log("Event", event)
            const { data } = await axiosPrivateInstance.get('auth/user');

            setUser(data)


        } catch (error) {
            console.log(error.response)
        }
    }

    return getUser
}
