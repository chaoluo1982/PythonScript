#include <iostream>
#include <string>
#include <vector>
#include <bitset>
#include <map>


    template <typename EnumLiteral>
    constexpr typename std::underlying_type<EnumLiteral>::type toUnderlying(EnumLiteral e) noexcept
    {
        return static_cast<typename std::underlying_type<EnumLiteral>::type>(e);
    }

int main()
{



    std::string ratString{"W L N NR NT"};
    
    enum class TrCarrierStandard
    {
    WCDMA,
    LTE_FDD,
    LTE_TDD,
    GSM,
    CDMA,
    NBIOT,
    NR_FDD,
    NR_TDD,
    NONE
    };
    
   class C1
    {
    public: 
        void f(int a)
        {
            return;
        }
    };

    typedef void(C1::*Func)(int);
    Func fm = &C1::C1::C1::f;
    C1 my;
    my.f(1);
    (my.*fm)(1);
    
   std::bitset<toUnderlying(TrCarrierStandard::NONE)> configuredRatTypes;

    struct                      // This horrible formatting is what 'codestyle' thinks is right!
    {
        std::string ratStr;
        TrCarrierStandard rat;
    } rats[] =
    {
        { "W",  TrCarrierStandard::WCDMA},
        { "L",  TrCarrierStandard::LTE_FDD },
        { "NB",  TrCarrierStandard::NBIOT },
        { "T",  TrCarrierStandard::LTE_TDD },
        { "G",  TrCarrierStandard::GSM },
        { "C",  TrCarrierStandard::CDMA },
        { "NF",  TrCarrierStandard::NR_FDD },
        { "NT", TrCarrierStandard::NR_TDD }
    };

    configuredRatTypes.reset();          // Reset selection. Only needed for the unit tests, really.



    {
        for (std::size_t i = 0; i < configuredRatTypes.size() ; i++)
        {
            if (ratString.find(rats[i].ratStr) != std::string::npos)
            {
                configuredRatTypes.set(toUnderlying(rats[i].rat));
            }
        }
    }

std::cout<<configuredRatTypes.size()<<'\n';
std::cout<<toUnderlying(TrCarrierStandard::NONE)<<'\n';


    std::cout<<configuredRatTypes.to_string()<<'\n';

    std::map<int, int> maps;
    std::cout<<maps[2];


}

