#include <array>
#include <type_traits>

namespace enhanced_enum {

template<
    typename EnhancedEnum, typename UnderlyingEnum, typename ValueType>
struct enum_base {
    static_assert( std::is_enum_v<UnderlyingEnum> );

    using enum_type = UnderlyingEnum;
    using value_type = ValueType;

    enum_base() = default;
    constexpr enum_base(UnderlyingEnum name) : name {name} {}

    constexpr enum_type get() const
    {
        return name;
    }

    constexpr const value_type& value() const
    {
        const auto n = static_cast<std::size_t>(name);
        return EnhancedEnum::values.at(n);
    }

private:
    UnderlyingEnum name;
};

template<typename Enum>
using enhanced = decltype(enhance(std::declval<Enum>()));

}
