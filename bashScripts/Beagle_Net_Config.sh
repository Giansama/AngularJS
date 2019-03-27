#!/bin/bash
if [ $(id -u) != "0" ]; then 
    echo "O Script não esta sendo executado com permissão root."
    echo "Note que esse Script precisa de sudo para funcionar"
    echo "Então execute novamente o programa com sudo"
else
    while true; do
	read -p "[*] Qual dispositivo deseja configurar, [H]ost ou [G]uest? " ans
    	case $ans in
		[hH]* ) 
		    i=0
		    for x in $(ip a | grep ": "| cut -d: -f2 | cut -d" " -f2); do
			net_list[$i]=$x
			((i++))
		    done
		    j=0
		    for y in $(ip a | grep "inet " | cut -d" " -f6); do
			echo "[$j] ${net_list[$j]} - $y"
			((j++))
		    done

		    while true; do
			echo ""
			while true; do
			    read -p "[.] Escolha qual a rede host. " label_host
			    if [[ ${net_list[$label_host]} != "" ]]; then
				break
			    else
				echo "[!] Host Inválida."	
			    fi
		    	done
		    	while true; do
		    	    read -p "[.] Escolha qual a rede guest. " label_guest
			    if [[ ${net_list[$label_guest]} != "" ]]; then
				break
		    	    else
				echo "[!] Guest Inválida."	
    			    fi
		    	done

			if [[ ${net_list[$label_host]} != ${net_list[$label_guest]} ]]; then
			    break
			else
			    echo "[!] As redes Host e Guest devem ser diferentes."
			fi
		    done
			
		    echo -e "\n[.] Confirme as informações antes de continuar."
		    echo "[.] Host  : ${net_list[$label_host]}"
		    echo "[.] Guest : ${net_list[$label_guest]}"
		    echo -n "[*] Pressione Enter para continuar ou Ctrl+c para abortar."
		    read check
		    
		    ifconfig ${net_list[$label_guest]} 192.168.7.1
		    iptables --table nat --append POSTROUTING --out-interface ${net_list[$label_host]} -j MASQUERADE
		    iptables --append FORWARD --in-interface ${net_list[$label_guest]} -j ACCEPT
		    echo 1 > /proc/sys/net/ipv4/ip_forward

		break;;
		
		
		[gG]* )
		    echo -n "[*] Pressione Enter para continuar ou Ctrl+c para abortar."
		    read check
		    
		    ifconfig usb0 192.168.7.2
		    route add default  gw 192.168.7.1
		    echo "nameserver 8.8.8.8" >> /etc/resolv.conf

		break;;
		
		
		* )
		    echo "[!] Por favor entre com uma opção válida.";;
  		esac
    done
    echo -e "\n[*] Configuração Concluída."
fi

