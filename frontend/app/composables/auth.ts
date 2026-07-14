


const auth = useState('auth', ()=>null)

export const useAuth = () => {

    const get = () => auth

    const set = (user) => {
        auth.value = user
    }

    return { get, set}

}

