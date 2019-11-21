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
    typename EnhancedEnum, typename LabelEnum, typename ValueType>
struct enum_base {
    static_assert( std::is_enum_v<LabelEnum> );

    using enum_type = LabelEnum;    ///< \brief Label enum type
    using value_type = ValueType;   ///< \brief Enhanced enum value type

    enum_base() = default;

    /** \brief Construct enhanced enum from a label enumerator
     */
    constexpr enum_base(LabelEnum label) noexcept : label {label} {}

    /** \brief Get the label enumerator
     */
    constexpr enum_type get() const
    {
        return label;
    }

    /** \brief Get the value of the enhanced enumerator
     */
    constexpr const value_type& value() const
    {
        const auto n = static_cast<std::size_t>(label);
        return EnhancedEnum::values.at(n);
    }

private:
    LabelEnum label;
};

/** \brief The enhanced enum type associated with a label enum type
 */
template<typename Enum>
using enhanced = decltype(enhance(std::declval<Enum>()));

}
