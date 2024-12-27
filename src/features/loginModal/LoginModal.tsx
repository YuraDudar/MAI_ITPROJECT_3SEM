import { Button } from "@/shared/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/shared/ui/dialog"
import { Input } from "@/shared/ui/input"
import { Label } from "@/shared/ui/label"
import PhoneInput from "@/shared/ui/phoneInput"
import { useEffect, useState } from "react"
import { Badge } from "@/shared/ui/badge"
import { useModalStore } from "@/shared/store/modalStore"
import { MODALS } from "@/shared/consts/modal"
import { useLogin } from "@/shared/hooks/useLogin"
import { Icon } from "@/shared/ui/icon"
import { LucideArrowLeft } from "lucide-react"
import { RegisterModalProps } from "../registerModal/RegisterModal"
 
export const LoginModal = () => {
  const {loginUser, isLoading, isIdle, data} = useLogin();
  const {openModals, openModal, closeModal} = useModalStore();
  const [isOpen, setIsOpen] = useState(openModals.has(MODALS.LOGIN));
  const [step, setStep] = useState(1);
  const [login, setLogin] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLoginButton = () => {
    if (step <= 1) {
      setStep(prev => prev + 1);
    } else {
      loginUser({email, password})
    }
  }

  const handleBackButtonClick = () => setStep(prev => prev - 1)

  const handleLoginChange = (value: string) => {
    setLogin(value);
  }

  const handlePasswordChange: React.ChangeEventHandler<HTMLInputElement> = (value) => {
    setPassword(value.target.value)
  }

  const handleEmailChange: React.ChangeEventHandler<HTMLInputElement> = (value) => {
    setEmail(value.target.value)
  }

  useEffect(() => {
    if (isLoading || isIdle) return;
    if (!data) {
      openModal({
        name: MODALS.REGISTRATION,
        props: {user: {email, password, username: login}} as RegisterModalProps
      })
    } else {
      localStorage.setItem('jwt', JSON.stringify(data.access_token));
      closeModal(MODALS.LOGIN);
      setIsOpen(false);
    }
  }, [isLoading])

  return (
    <Dialog open={isOpen}>
      <DialogContent className="sm:max-w-[724px] p-10 gap-[13px] bg-white">
        <DialogHeader>
          <DialogTitle className="mb-8">
            <Icon size={262} icon="logo" />
          </DialogTitle>
          <DialogDescription>
            {step === 1 && (
              <div className="flex flex-col gap-[13px]">
                <p className="text-[26px]">Введите номер телефона</p>
                <p>Мы отправим вам код по СМС или на электронную почту. Отвечать на звонок не потребуется.</p>
              </div>
            )}
            {step === 2 && (
              <div className="flex flex-col gap-2">
                <p className="font-bold text-[26px]">Введите последние 6 цифр входящего номера</p>
                <div className="flex gap-2">
                  <p>Например +7 XXX X</p>
                  <Badge className="border-[#FF9874]" variant="outline">
                    <p className="text-[#FF9874]">14 89 52</p>
                  </Badge>
                </div>
                <p>Отвечать на звонок не нужно</p>
              </div>
            )}
          </DialogDescription>
        </DialogHeader>
        {step === 1 && (
          <div className="grid gap-4 grid-cols-2">
            <PhoneInput className="flex-1 h-full" value={login} defaultCountry="RU" onChange={handleLoginChange} id="phone" />
            <Label className="flex-1 text-[32px] h-full! flex justify-start items-center leading-1 border-gray-100 border-2 rounded-lg pl-2" htmlFor="phone"><LucideArrowLeft /> USERNAME</Label>
            <Input className="flex-1 h-full" value={email} onChange={handleEmailChange} placeholder="123@123.com" id="email" />
            <Label className="flex-1 text-[32px] h-full! flex justify-start items-center leading-1 border-gray-100 border-2 rounded-lg pl-2" htmlFor="email"><LucideArrowLeft /> EMAIL</Label>
          </div>
        )}
        {step === 2 && (
          <div>
            <Input value={password} onChange={handlePasswordChange} />
          </div>
        )}
        <DialogFooter className="flex content-between">
          {step > 1 && (
            <Button className="bg-[#FF9874] flex-1" onClick={handleBackButtonClick}>
              <p className="font-light text-white uppercase">Назад</p>
            </Button>
          )}
          <Button disabled={(step === 1 && !login.length || step === 2 && !password.length)} className="bg-[#FF9874] flex-1" onClick={handleLoginButton}>
            <p className="font-light text-white uppercase">Войти</p>
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
