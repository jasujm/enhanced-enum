#include <array>
#include <compare>
#include <tuple>

#include "status.hh"

using testapp::StatusLabel;
using testapp::EnhancedStatus;
namespace Statuses = testapp::Statuses;

static_assert( (Statuses::BUSY <=> StatusLabel::BUSY) == std::strong_ordering::equal );
static_assert( (StatusLabel::BUSY <=> Statuses::BUSY) == std::strong_ordering::equal );
static_assert( (Statuses::BUSY <=> Statuses::BUSY) == std::strong_ordering::equal );

static_assert( (Statuses::INITIALIZING <=> StatusLabel::BUSY) == std::strong_ordering::less );
static_assert( (StatusLabel::INITIALIZING <=> Statuses::BUSY) == std::strong_ordering::less );
static_assert( (Statuses::INITIALIZING <=> Statuses::BUSY) == std::strong_ordering::less );

static_assert( (Statuses::BUSY <=> StatusLabel::INITIALIZING) == std::strong_ordering::greater );
static_assert( (StatusLabel::BUSY <=> Statuses::INITIALIZING) == std::strong_ordering::greater );
static_assert( (StatusLabel::BUSY <=> Statuses::INITIALIZING) == std::strong_ordering::greater );
