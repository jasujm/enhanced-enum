/** \file
 */

#include <array>
#include <type_traits>

/** \brief The ennhanced enum library
 */
namespace enhanced_enum {

/** \brief Base class for enhanced enum types
 */
template<
    typename EnhancedEnum, typename UnderlyingEnum, typename ValueType>
struct enum_base {
    static_assert( std::is_enum_v<UnderlyingEnum> );

    using enum_type = UnderlyingEnum; ///< \brief Underlying enum type
    using value_type = ValueType;     ///< \brief Enhanced enum value type

    enum_base() = default;

    /** \brief Construct enhanced enum from an underlying enumerator
     */
    constexpr enum_base(UnderlyingEnum name) : name {name} {}

    /** \brief Get the underlying enumerator
     */
    constexpr enum_type get() const
    {
        return name;
    }

    /** \brief Get the value of the enhanced enumerator
     */
    constexpr const value_type& value() const
    {
        const auto n = static_cast<std::size_t>(name);
        return EnhancedEnum::values.at(n);
    }

private:
    UnderlyingEnum name;
};

/** \brief The enhanced enum type associated with an underlying enum type
 */
template<typename Enum>
using enhanced = decltype(enhance(std::declval<Enum>()));

}
